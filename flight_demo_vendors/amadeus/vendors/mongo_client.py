# mongo_client.py
from pymongo import MongoClient
import re
from bson import ObjectId

client = MongoClient("mongodb://localhost:27019/")
db = client["flights"]
bookings_collection = db["bookings"]
sabre_collection = db["sabre"]
amadeus_collection = db["amadeus"]


def convert_object_id(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc


def get_all_bookings(user_id):
    upcoming = list(bookings_collection.find({"userId": user_id, 'status': 'UPCOMING'}).sort("travel_date", 1))
    complete = list(bookings_collection.find({"userId": user_id, 'status': 'COMPLETED'}).sort("update_time", -1))
    cancelled = list(bookings_collection.find({"userId": user_id, 'status': 'CANCELLED'}).sort("update_time", -1))
    result = {
        "upcoming": [convert_object_id(doc) for doc in upcoming],
        "complete": [convert_object_id(doc) for doc in complete],
        "cancelled": [convert_object_id(doc) for doc in cancelled]
    }
    return result


def get_flights_from_mongo(source, destination, start, end, vendor_name, sort_by="price", flight_sort_by="flightNumber"):
    source = re.compile(re.escape(source), re.IGNORECASE)
    destination = re.compile(re.escape(destination), re.IGNORECASE)
    if vendor_name == "Sabre":
        result = list(sabre_collection.find({"from": source, "to": destination}).sort([(flight_sort_by, 1),(sort_by, 1)]))
        return [convert_object_id(doc) for doc in result]
    if vendor_name == "Amadeus":
        result =  list(amadeus_collection.find({"from": source, "to": destination}).sort([(flight_sort_by, 1),(sort_by, 1)]).skip(start).limit(end))
        return [convert_object_id(doc) for doc in result]
    return list()


def search_cities_by_keyword(keyword, from_param=None):
    if not keyword or len(keyword) <= 2:
        return []

    regex = re.compile(re.escape(keyword), re.IGNORECASE)
    if from_param and from_param != 'null' and len(from_param) > 2:
        from_param_regex = re.compile(re.escape(from_param), re.IGNORECASE)
        destinations = set()
        destinations.update(sabre_collection.distinct("to", {"from": from_param_regex, "to": regex}))
        destinations.update(amadeus_collection.distinct("to", {"from": from_param_regex, "to": regex}))
        return sorted(destinations)
    else:
        # Combine 'from' and 'to' cities matching the keyword
        sources = sabre_collection.distinct("from", {"from": regex})
        destinations = sabre_collection.distinct("to", {"to": regex})
        sources += amadeus_collection.distinct("from", {"from": regex})
        destinations += amadeus_collection.distinct("to", {"to": regex})
        all_cities = set(sources + destinations)
        return sorted(all_cities)
