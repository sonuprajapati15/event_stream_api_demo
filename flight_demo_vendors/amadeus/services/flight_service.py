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

def generate_flight(i):
    from_city, to_city, layover = get_random_international_route_with_layover()
    return {
        "flightId": f"FLIGHT-{3000 + i}",
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
        "vendor_name": 'Amadeus',
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
    flights =  get_flights_from_mongo(source, destination, start, end, 'Amadeus')
    for flight in flights:
        for cat in flight['fareCategories']:
            cat['fareOptions'] = sorted(cat['fareOptions'], key=lambda x: x.get('total_price', 0))
    return flights

def get_fare_categories(price):
    return [
        forRecommeded(price, {}),
        forValueOne(price, {}),
        forExpensiveOnbe(price, {})
    ]