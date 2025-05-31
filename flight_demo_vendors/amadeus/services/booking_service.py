from vendors.mongo_client import get_all_bookings, bookings_collection
from flask import jsonify

def get_all_bookings_service(userid):
    return get_all_bookings(userid)

def save_booking_service(request):
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