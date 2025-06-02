import random
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


cityImages = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn1h0du7X6cxnkLHYCmxGEYRIWvWPGqCqz6JfzD_xZ0hdi7_ui493o81U4MKVt5BfJ-M0&usqp=CAU',
              'https://img.etimg.com/thumb/msid-116567353,width-480,height-360,imgsize-2457160,resizemode-75/hill-stations-for-snow-near-delhi.jpg',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrl1qpvRFgajjpjE-sZ-8lV-sSmPuzq-eTrCFeiQBnrG6FjOaTqTbZwtVLCUgVxW99DYI&usqp=CAU',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzoDRR1PH9z_zbX5Ty64reEk1ulS2OtZfxNAxi0NlEtGOmIWOkd4QuRoA0NxD3jypaW6w&usqp=CAU'
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0P854_yeZEn-NP0HTZKBdSx55CkbZHqfGTMlNWbl0DU1tUbv1xRN3gmuov0H5umf1vP8&usqp=CAU',
              'https://www.tourism-of-india.com/blog/wp-content/uploads/2018/06/Pelling-Sikkim.jpg',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS97BgOXzc2JikXg9s9V0SrtJMhogl0YShYRWJe1l0IXkUTYFf1hD-1el_DUD9OMy6Xjic&usqp=CAU',
              'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8uK8UaDGEAn_8VrsGnV1smKjUFjCEgLm4xg&s'
              ]

def get_all_bookings_service(userid):
    bookingStatusMap =  get_all_bookings(userid)
    for key in bookingStatusMap:
        for booking in bookingStatusMap.get(key):
            if isinstance(booking, dict):
                booking['cityImage'] = choice(bgImage) if random.randint(1, 2) == 1 else choice(cityImages)
                booking['bgImage'] = choice(bgImage) if random.randint(1, 2) == 1 else choice(cityImages)
    return bookingStatusMap


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
