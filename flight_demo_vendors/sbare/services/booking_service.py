from datetime import datetime, timedelta
from vendors.mongo_client import get_all_bookings, bookings_collection
from flask import jsonify
from flight_demo_vendors.sbare.services.flight_service import get_flights_from_db_by_id


def get_all_bookings_service(userid):
    return get_all_bookings(userid)


def save_booking_service(request):
    booking = request.get_json()
    user_id = booking.get('userId')
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        return jsonify({"error": "Missing or invalid userId parameter"}), 400
    flight_data = get_flights_from_db_by_id(booking.get('flightId'), booking.get('fareType'), booking.get('fareId'))
    if isinstance(flight_data, dict):
        booking.update(flight_data)
    booking.pop('_id', None)
    booking["date_time"] = datetime.now().isoformat()
    booking["update_time"] = datetime.now().isoformat()
    booking["travel_date"] = (datetime.now() + timedelta(days=32)).isoformat()

    if booking.get("lobName") is None:
        booking["lobName"] = "FLIGHT"
    if booking.get("status") is None:
        booking["status"] = "UPCOMING"
    try:
        result = bookings_collection.insert_one(booking)
        booking['_id'] = str(result.inserted_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Booking saved successfully", "booking": booking}), 201
