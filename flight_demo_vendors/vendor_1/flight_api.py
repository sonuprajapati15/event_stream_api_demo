from flask import Flask, jsonify, request
import random
import json
from time import sleep
from datetime import datetime, timedelta
from flight_demo_vendors.mongo_client import get_all_bookings, get_flights_from_mongo, search_cities_by_keyword, bookings_collection

app = Flask(__name__)

airlines = [{"name":"IndiGo", "logo":"https://www.liblogo.com/img-logo/in7716i6b7-indigo-logo-indigo-is-hiring-for-trainee-qa-amp-ts-apply-now.png"},
            {"name":"Air India","logo":"https://tse1.mm.bing.net/th/id/OIP.VF8rQObGF-vhG_BQLL0zmgHaEo?rs=1&pid=ImgDetMain"},
            {"name":"SpiceJet", "logo":"https://tse3.mm.bing.net/th/id/OIP.2FAwuoQcqTrxpgdMyQrMmgAAAA?rs=1&pid=ImgDetMain"},
            {"name":"Vistara", "logo":"https://tse4.mm.bing.net/th/id/OIP.1AJghOmsWxb_Z2FklliYgAHaE8?rs=1&pid=ImgDetMain"},
            {"name":"Go First", "logo":"https://www.odishaage.com/wp-content/uploads/2021/08/GO-FIRST.png"},
            {"name":"Akasa Air", "logo":"https://tse1.mm.bing.net/th/id/OIP.racldovE1XyYS-S_4FP3QQHaBQ?rs=1&pid=ImgDetMain"},
            {"name":"Lufthansa ", "logo":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv9X0JBcHTs4fb6SI2MGsl0Jn1bMycfs49nQ&s"},
            {"name":"British Airways", "logo":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQv3If5jF-HB-7Ky2l99w0ZsGovIeFREY98Wg&s"},
            {"name":"Etihad Airways", "logo":"https://images.seeklogo.com/logo-png/17/2/etihad-airways-logo-png_seeklogo-177330.png"}
            ]
seat_types = ["Economy", "Premium Economy", "Business", "First Class"]
cabin_classes = ["Standard", "Premium", "Deluxe", "Executive"]
flight_types = ["Non-Stop", "One-Stop", "Two-Stop"]
baggage_options = ["Cabin Only", "Cabin + 15kg Checked", "Cabin + 25kg Checked", "Cabin + 30kg Checked"]
cancellation_policies = ["Refundable", "Non-Refundable", "Partially Refundable"]
change_policies = ["Free Changes", "Fee Applies", "Not Allowed"]
meal_options = ["Vegetarian", "Non-Vegetarian", "Jain", "No Meal"]
wifi_availability = ["Available", "Not Available"]
entertainment_options = ["In-Flight Entertainment", "Streaming via App", "None"]
aircraft_types = ["Airbus A320", "Boeing 737", "Airbus A321", "Boeing 787"]
fare_classes = ["Y", "B", "M", "H", "Q", "K"]
gate_numbers = [f"A{n}" for n in range(1, 21)]

def get_random_international_route_with_layover():
    layover_cities = ["Hyderabad", "Ahmedabad", "Chennai", "Bengaluru", "Pune", "Kolkata"]
    from_cities = ["Delhi", "dubai", "london", "new york", "germany", "canada", "singapore", "france", "switzerland", "australia"]
    to_cities = ["Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Goa", "Cochin"]

    valid_from = [city for city in from_cities if city not in layover_cities]
    valid_to = [city for city in to_cities if city not in layover_cities]

    from_city = random.choice(valid_from)
    to_city = random.choice([city for city in valid_to if city != from_city])

    possible_layovers = [city for city in layover_cities if city != from_city and city != to_city]
    layover = random.choice(possible_layovers) if possible_layovers and random.choice([True, False]) else None
    return from_city, to_city, layover


def random_time():
    start = datetime.strptime('00:00', '%H:%M')
    end = datetime.strptime('23:59', '%H:%M')
    rand_minutes = random.randint(0, int((end - start).total_seconds() // 60))
    return (start + timedelta(minutes=rand_minutes)).strftime('%H:%M')

def generate_flight(i):
    from_city, to_city, layover = get_random_international_route_with_layover()
    return {
        "flightId": f"FLIGHT-{4103 + i}",
        "flightNumber": f"{random.choice(airlines)['name'][:2].upper()}-{random.randint(100, 9999)}",
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
        "totalStops": 1,
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

@app.route('/vendor1/api/flights', methods=['GET'])
def get_flights():
    flights = [generate_flight(i) for i in range(2000)]
    return jsonify(flights)

@app.route('/vendor1/api/flights/paginated', methods=['GET'])
def get_flights_paginated():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))
    start = (page - 1) * per_page
    end = start + per_page
    sleep(2) # adding delay of 2 sec
    try:
        with open("all_flights_data.json", "r") as f:
            all_flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "page": page,
        "perPage": per_page,
        "totalFlights": len(all_flights),
        "flights": all_flights[start:end]
    })


@app.route('/vendor1/api/flights/search', methods=['GET'])
def search_flights():
    source = request.args.get('from')
    destination = request.args.get('to')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))

    if not source or not destination:
        return jsonify({"error": "Missing 'from' or 'to' parameter"}), 400

    flights = get_flights_from_mongo(source, destination, 'Amadeus')
    sorted_flights = sorted(flights, key=lambda x: x['price'])
    start = (page - 1) * per_page
    end = start + per_page
    paginated_flights = sorted_flights[start:end]

    return jsonify({
        "page": page,
        "perPage": per_page,
        "totalFlights": len(sorted_flights),
        "flights": paginated_flights
    })

@app.route('/vendor1/api/bookings', methods=['GET'])
def get_bookings_by_route():
    userid = request.args.get('userId')
    if not userid:
        return jsonify({"error": "Missing userid parameter"}), 400
    return jsonify(get_all_bookings(userid, 'Amadeus'))


@app.route('/vendor1/api/cities/search', methods=['GET'])
def search_cities():
    keyword = request.args.get('keyword')
    if not keyword or len(keyword) <= 2:
        return jsonify({"error": "Parameter 'keyword' is required and must be at least 3 characters long."}), 400
    from_param = request.args.get('from')
    cities = search_cities_by_keyword(keyword, from_param)
    return jsonify({"cities": cities})


@app.route('/vendor1/api/bookings', methods=['POST'])
def save_booking():
    user_id = request.args.get('userId')
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        return jsonify({"error": "Missing or invalid userId parameter"}), 400

    booking = request.get_json()
    if not booking or not isinstance(booking, dict):
        return jsonify({"error": "Invalid booking data"}), 400

    booking['userId'] = user_id

    try:
        result = bookings_collection.insert_one(booking)
        booking['_id'] = str(result.inserted_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Booking saved successfully", "booking": booking}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
