from vendors.mongo_client import get_all_bookings, bookings_collection
from services.flight_service import get_flights_from_db_by_id
from flask import jsonify

def get_all_bookings_service(userid):
    return get_all_bookings(userid)

def save_booking_service(request):
    booking = request.get_json()
    user_id = booking['userId']
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        return jsonify({"error": "Missing or invalid userId parameter"}), 400
    flight_data = get_flights_from_db_by_id(booking['flightId'], booking['fareType'], booking['fareId'])
    booking['flight_info'] = flight_data
    try:
        result = bookings_collection.insert_one(booking)
        booking['_id'] = str(result.inserted_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Booking saved successfully", "booking": booking}), 201