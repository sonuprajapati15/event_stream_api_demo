import random
import json
from datetime import datetime, timedelta
from flask import jsonify
from vendors.mongo_client import get_flights_from_mongo
from utils.random_utils import (
    get_random_international_route_with_layover, random_time, airlines, seat_types, cabin_classes, 
    flight_types, baggage_options, cancellation_policies, change_policies, meal_options, 
    wifi_availability, entertainment_options, aircraft_types, fare_classes, gate_numbers
)
from utils.fare_utils import forRecommeded, forValueOne, forExpensiveOnbe

from flight_demo_vendors.amadeus.vendors.mongo_client import sabre_collection, convert_object_id

cityImages = ['https://img.freepik.com/free-photo/big-city_1127-3102.jpg?semt=ais_hybrid&w=740',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWT-7DycWq2GLmonKXV2v4VAvdpomwMKiXZA&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNEhjJyN1eHdHKBOQlq8-M7JPizJ2uGFYKU1ttNm0j5iAPME9j-ksYajv1-zF2ox8eauQ&usqp=CAU',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQco5Oky_Kg1I3k-x2j4mGpXgh_TNl9TTKSDA&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfeQEfsuNFN30EObu3WOA9cSl6Qo6FBOGz8A&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfeQEfsuNFN30EObu3WOA9cSl6Qo6FBOGz8A&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQF2WD9tYHASBteiggXecBLb6MxizagBu4SQ&s'
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZUIWKrXEuWwnVJkKKG2hQyu7Aja-vBqq__g&s']


bgImage = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpbcOB0Y8MuRIr2QUAc-knC_VZWYn6Jt-V_w&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQF2WD9tYHASBteiggXecBLb6MxizagBu4SQ&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ40FtCvdfhsg9gL5g0vWJobEODd43pJqs9Dw&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJJaqQiZIWe0GW3snZP48XVcqlv4490yugbg&s'
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN14T7Zr2DNPo7yqT0jR4fI6FUuticTyeqCw&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkY442bF8NRNPhzk1ihpOtTbQnoi4U5GS-DA&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwb9sN8F1MbvnVFpYJ_kq0t2esLW5XXTdU3g&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMw7uDKjS8qaabv97K3dEMDECi9rBai-_nQw&s'
              ]


def generate_flight(i):
    from_city, to_city, layover = get_random_international_route_with_layover()
    return {
        "flightId": f"FLIGHT-{5000 + i}",
        "flightNumber": f"{random.choice(airlines)['name'][:2].upper()}-{random.randint(100, 1000)}",
        "airline": random.choice(airlines),
        "from": from_city,
        "to": to_city,
        "departureTime": random_time(),
        "arrivalTime": random_time(),
        "duration": f"{random.randint(1, 5)}h {random.randint(0, 59)}m",
        "seatType": random.choice(seat_types),
        "cabinClass": random.choice(cabin_classes),
        "flightType": random.choice(flight_types),
        "baggage": random.choice(baggage_options),
        "cancellationPolicy": random.choice(cancellation_policies),
        "changePolicy": random.choice(change_policies),
        "price": random.randint(3000, 20000),
        "date": (datetime.today() + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
        "meal": random.choice(meal_options),
        "wifi": random.choice(wifi_availability),
        "entertainment": random.choice(entertainment_options),
        "aircraftType": random.choice(aircraft_types),
        "fareClass": random.choice(fare_classes),
        "gate": random.choice(gate_numbers),
        "terminal": f"T{random.randint(1, 3)}",
        "boardingTime": random_time(),
        "checkInCounter": f"C{random.randint(1, 20)}",
        "layovers": [layover],
        "totalStops": len(layover),
        "onTimePerformance": f"{random.randint(80, 99)}%",
        "seatPitch": f"{random.randint(28, 34)} inches",
        "seatWidth": f"{random.randint(17, 21)} inches",
        "recliningAngle": f"{random.randint(10, 30)} degrees",
        "powerOutlet": random.choice(["Yes", "No"]),
        "usbPort": random.choice(["Yes", "No"]),
        "priorityBoarding": random.choice(["Yes", "No"]),
        "loungeAccess": random.choice(["Yes", "No"]),
        "extraLegroom": random.choice(["Yes", "No"]),
        "petPolicy": random.choice(["Allowed", "Not Allowed"]),
        "infantPolicy": random.choice(["Free", "Chargeable"]),
        "covidSafety": random.choice(["High", "Moderate", "Low"]),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "reviewsCount": random.randint(10, 1000),
        "ecoFriendly": random.choice(["Yes", "No"]),
        "lastUpdated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "vendor_name": 'Sabre',
        "vendor_logo": 'https://tse3.mm.bing.net/th/id/OIP.zMXaa5KC0DWwQVo4FxgragHaBL?rs=1&pid=ImgDetMain'
    }

def group_by_flight(flights, group_by='flightNumber'):
    from collections import defaultdict
    grouped = defaultdict(list)
    for flight in flights:
        grouped[flight[group_by]].append(flight)
    return list(grouped.values())

def get_flights_from_file(page, per_page):
    from time import sleep
    sleep(2)
    try:
        with open("all_flights_data.json", "r") as f:
            all_flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({
        "page": page,
        "perPage": per_page,
        "totalFlights": len(all_flights),
        "flights": all_flights[start:end]
    })

def get_flights_from_db(source, destination, start=0, end=30):
    flights =  get_flights_from_mongo(source, destination, start, end, 'Sabre')
    for flight in flights:
        for cat in flight['fareCategories']:
            cat['fareOptions'] = sorted(cat['fareOptions'], key=lambda x: x.get('total_price', 0))
    return flights

def get_flights_from_db_by_id(flightId, fareCategoryName, fareCategoryId):
    if (
            flightId == 'undefined' or len(flightId) < 5 or
            fareCategoryName == 'undefined' or len(fareCategoryName) < 5 or
            fareCategoryId == 'undefined'
    ):
        return jsonify({"error": "Invalid flightId"}), 400
    flight = sabre_collection.find_one({'flightId': flightId})
    if not flight:
        return jsonify({"error": "Flight not found"}), 404
    try:
        for fareCategory in flight['fareCategories']:
            if fareCategory['fareType'] == fareCategoryName:
                flight['chooseFare'] = fareCategory['fareOptions'][int(fareCategoryId)]
                flight['image'] = fareCategory['image']
                break
    except (KeyError, IndexError, ValueError):
        return jsonify({"error": "Invalid fare category or ID"}), 400
    flight['fareCategories'] = None
    flight['bgImage'] = random.choice(bgImage)
    flight['cityImage'] = random.choice(cityImages)
    return convert_object_id(flight)

def get_fare_categories(price):
    return [
        forRecommeded(price, {}),
        forValueOne(price, {}),
        forExpensiveOnbe(price, {})
    ]