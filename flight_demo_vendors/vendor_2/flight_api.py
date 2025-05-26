import json
from time import sleep

from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)

airlines = [{"name":"IndiGo", "logo":"https://www.liblogo.com/img-logo/in7716i6b7-indigo-logo-indigo-is-hiring-for-trainee-qa-amp-ts-apply-now.png"},
            {"name":"Air India","logo":"https://tse1.mm.bing.net/th/id/OIP.VF8rQObGF-vhG_BQLL0zmgHaEo?rs=1&pid=ImgDetMain"},
            {"name":"SpiceJet", "logo":"https://tse3.mm.bing.net/th/id/OIP.2FAwuoQcqTrxpgdMyQrMmgAAAA?rs=1&pid=ImgDetMain"},
            {"name":"Vistara", "logo":"https://tse4.mm.bing.net/th/id/OIP.1AJghOmsWxb_Z2FklliYgAHaE8?rs=1&pid=ImgDetMain"},
            {"name":"Go First", "logo":"https://www.odishaage.com/wp-content/uploads/2021/08/GO-FIRST.png"}, {"name":"Akasa Air", "logo":"https://tse1.mm.bing.net/th/id/OIP.racldovE1XyYS-S_4FP3QQHaBQ?rs=1&pid=ImgDetMain"}]
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
layover_cities = ["Hyderabad", "Ahmedabad", "Chennai", "Bengaluru", "Pune", "Kolkata"]

def random_time():
    start = datetime.strptime('00:00', '%H:%M')
    end = datetime.strptime('23:59', '%H:%M')
    rand_minutes = random.randint(0, int((end - start).total_seconds() // 60))
    return (start + timedelta(minutes=rand_minutes)).strftime('%H:%M')

def generate_flight(i):
    layover_count = random.choice([0, 1, 2])
    layovers = random.sample(layover_cities, layover_count)
    return {
        "flightId": f"FLIGHT-{1000 + i}",
        "flightNumber": f"{random.choice(airlines)['name'][:2].upper()}-{random.randint(100, 9999)}",
        "airline": random.choice(airlines),
        "from": "Delhi",
        "to": "Mumbai",
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
        "layovers": layovers,
        "totalStops": len(layovers),
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
        "vendor_logo": 'https://download.logo.wine/logo/Sabre_Corporation/Sabre_Corporation-Logo.wine.png'
    }

@app.route('/vendor2/api/flights', methods=['GET'])
def get_flights():
    flights = [generate_flight(i) for i in range(40)]
    return jsonify(flights)

@app.route('/vendor2/api/flights/paginated', methods=['GET'])
def get_flights_paginated():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))

    start = (page - 1) * per_page
    end = start + per_page

    try:
        with open("all_flights_data.json", "r") as f:
            all_flights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500

    sleep(1) # adding delay of 1 sec

    return jsonify({
        "page": page,
        "perPage": per_page,
        "totalFlights": len(all_flights),
        "flights": all_flights[start:end]
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)
