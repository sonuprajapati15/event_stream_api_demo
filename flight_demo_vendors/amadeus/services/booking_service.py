from datetime import datetime, timedelta
from random import choice

from vendors.mongo_client import get_all_bookings, bookings_collection, convert_object_id
from flask import jsonify
from flight_demo_vendors.amadeus.services.flight_service import get_flights_from_db_by_id


bgImage = ['https://img.freepik.com/free-photo/big-city_1127-3102.jpg?semt=ais_hybrid&w=740',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWT-7DycWq2GLmonKXV2v4VAvdpomwMKiXZA&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNEhjJyN1eHdHKBOQlq8-M7JPizJ2uGFYKU1ttNm0j5iAPME9j-ksYajv1-zF2ox8eauQ&usqp=CAU',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQco5Oky_Kg1I3k-x2j4mGpXgh_TNl9TTKSDA&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfeQEfsuNFN30EObu3WOA9cSl6Qo6FBOGz8A&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfeQEfsuNFN30EObu3WOA9cSl6Qo6FBOGz8A&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQF2WD9tYHASBteiggXecBLb6MxizagBu4SQ&s'
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZUIWKrXEuWwnVJkKKG2hQyu7Aja-vBqq__g&s']


cityImages = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpbcOB0Y8MuRIr2QUAc-knC_VZWYn6Jt-V_w&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQF2WD9tYHASBteiggXecBLb6MxizagBu4SQ&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ40FtCvdfhsg9gL5g0vWJobEODd43pJqs9Dw&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJJaqQiZIWe0GW3snZP48XVcqlv4490yugbg&s'
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN14T7Zr2DNPo7yqT0jR4fI6FUuticTyeqCw&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkY442bF8NRNPhzk1ihpOtTbQnoi4U5GS-DA&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwb9sN8F1MbvnVFpYJ_kq0t2esLW5XXTdU3g&s',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMw7uDKjS8qaabv97K3dEMDECi9rBai-_nQw&s'
              ]

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
    booking["date_time"] = datetime.now()
    booking.pop('_id', None)
    booking["update_time"] = datetime.now()
    booking["travel_date"] = datetime.now() + timedelta(days=30)

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

def getBookingByTicketId(ticketId):
    if not ticketId or not isinstance(ticketId, str) or not ticketId.strip():
        return jsonify({"error": "Missing or invalid ticketId parameter"}), 400
    booking = bookings_collection.find_one({"ticketNo": ticketId})
    if booking:
        booking = convert_object_id(booking)
        booking['cityImage'] = choice(cityImages)
        booking['bgImage'] = choice(bgImage)
        return booking
    else:
        return {"error": "Booking not found"}
