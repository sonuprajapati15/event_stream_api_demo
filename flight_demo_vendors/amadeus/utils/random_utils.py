import random
from datetime import datetime, timedelta

airlines = [
    {"name":"IndiGo", "logo":"https://www.liblogo.com/img-logo/in7716i6b7-indigo-logo-indigo-is-hiring-for-trainee-qa-amp-ts-apply-now.png"},
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
    layover_cities = ["",
        "Hyderabad", "Ahmedabad", "Chennai", "Bengaluru", "Pune", "Kolkata", "Istanbul", "Frankfurt", "Doha",
        "Singapore","Bangkok", "Abu Dhabi", "Muscat", "Kuala Lumpur", "Hong Kong", "Dubai", "London", "Paris", "Zurich",
        "Amsterdam","Madrid", "Munich", "Vienna", "Brussels", "Rome", "Moscow", "Beijing", "Shanghai", "Seoul", "Tokyo",
        "Los Angeles","San Francisco", "Chicago", "Atlanta", "Dallas", "Miami", "Toronto", "Vancouver", "Montreal", "Mexico City",
        "Sao Paulo", "Buenos Aires", "Johannesburg", "Cape Town", "Nairobi", "Cairo", "Istanbul", "Doha", "Doha",
        "Manila", "Jakarta", "Sydney", "Melbourne", "Perth", "Brisbane", "Auckland", "Christchurch", "Wellington",
        "Fiji", "Male", "Hanoi", "Ho Chi Minh City", "Phnom Penh", "Yangon", "Colombo", "Kathmandu", "Dhaka", "Karachi",
        "Lahore", "Islamabad", "Jeddah", "Riyadh", "Medina", "Kuwait City", "Amman", "Tel Aviv", "Tehran", "Baghdad",
        "Damascus", "Beirut", "Addis Ababa", "Accra", "Lagos", "Casablanca", "Algiers", "Tunis", "Rabat", "Lisbon",
        "Oslo", "Stockholm", "Copenhagen", "Helsinki", "Warsaw", "Prague", "Budapest", "Bucharest", "Sofia", "Belgrade"
    ]
    from_cities = [
        "Delhi", "Dubai", "London", "New York", "Frankfurt", "Singapore", "Paris", "Zurich", "Sydney", "Melbourne",
        "Brisbane", "Perth", "Auckland", "Doha", "Istanbul", "Abu Dhabi", "Muscat", "Kuala Lumpur", "Hong Kong",
        "Tokyo", "Shanghai", "Beijing", "Seoul", "Bangkok", "Los Angeles", "San Francisco", "Chicago", "Toronto",
        "Vancouver", "Montreal", "Madrid", "Munich", "Vienna", "Brussels", "Rome", "Moscow", "Cairo", "Johannesburg",
        "Cape Town", "Nairobi", "Mexico City", "Sao Paulo", "Buenos Aires", "Jeddah", "Riyadh", "Amman", "Tel Aviv",
        "Tehran", "Baghdad", "Damascus", "Beirut", "Addis Ababa", "Accra", "Lagos", "Casablanca", "Algiers", "Tunis",
        "Rabat", "Lisbon", "Oslo", "Stockholm", "Copenhagen", "Helsinki", "Warsaw", "Prague", "Budapest", "Bucharest",
        "Sofia", "Belgrade", "Karachi", "Lahore", "Islamabad", "Kolkata", "Hyderabad", "Ahmedabad", "Chennai", "Pune",
        "Bengaluru", "Goa", "Jaipur", "Cochin", "Goa", "Male", "Fiji", "Wellington", "Christchurch", "Hanoi",
        "Ho Chi Minh City", "Phnom Penh", "Yangon", "Colombo", "Kathmandu", "Dhaka", "Geneva", "Barcelona", "Venice"
    ]
    to_cities = [
        "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Goa", "Cochin",
        "Delhi", "Dubai", "London", "New York", "Frankfurt", "Singapore", "Paris", "Zurich", "Sydney", "Melbourne",
        "Brisbane", "Perth", "Auckland", "Doha", "Istanbul", "Abu Dhabi", "Muscat", "Kuala Lumpur", "Hong Kong",
        "Tokyo", "Shanghai", "Beijing", "Seoul", "Bangkok", "Los Angeles", "San Francisco", "Chicago", "Toronto",
        "Vancouver", "Montreal", "Madrid", "Munich", "Vienna", "Brussels", "Rome", "Moscow", "Cairo", "Johannesburg",
        "Cape Town", "Nairobi", "Mexico City", "Sao Paulo", "Buenos Aires", "Jeddah", "Riyadh", "Amman", "Tel Aviv",
        "Tehran", "Baghdad", "Damascus", "Beirut", "Addis Ababa", "Accra", "Lagos", "Casablanca", "Algiers", "Tunis",
        "Rabat", "Lisbon", "Oslo", "Stockholm", "Copenhagen", "Helsinki", "Warsaw", "Prague", "Budapest", "Bucharest",
        "Sofia", "Belgrade", "Karachi", "Lahore", "Islamabad", "Male", "Fiji", "Wellington", "Christchurch", "Hanoi",
        "Ho Chi Minh City", "Phnom Penh", "Yangon", "Colombo", "Kathmandu", "Dhaka", "Geneva", "Barcelona", "Venice"
    ]
    valid_from = [city for city in from_cities if city not in layover_cities]
    valid_to = [city for city in to_cities if city not in layover_cities]
    from_city = random.choice(valid_from)
    to_city = random.choice([city for city in valid_to if city != from_city])
    possible_layovers = [city for city in layover_cities if city != from_city and city != to_city]
    layover = [random.choice(possible_layovers)] if possible_layovers and random.choice([True, False]) else []
    return from_city, to_city, layover

def random_time():
    start = datetime.strptime('00:00', '%H:%M')
    end = datetime.strptime('23:59', '%H:%M')
    rand_minutes = random.randint(0, int((end - start).total_seconds() // 60))
    return (start + timedelta(minutes=rand_minutes)).strftime('%H:%M')