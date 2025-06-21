from flask import Blueprint, jsonify, request
from flight_demo_vendors.amadeus.services.booking_service import get_all_bookings_service, save_booking_service, getBookingByTicketId
import datetime
from dateutil import parser  # pip install python-dateutil

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def get_bookings_by_route():
    userid = request.args.get('userId')
    if not userid:
        return jsonify({"error": "Missing userid parameter"}), 400

    bookingsByStatus = get_all_bookings_service(userid)

    result = {
        "upcoming": merge_connected_trips(bookingsByStatus.get('upcoming'), 'upcoming'),
        "complete": merge_connected_trips(bookingsByStatus.get('complete'), 'complete'),
        "cancelled": convertToConnectedResponse(bookingsByStatus.get('cancelled')),
        "failed": convertToConnectedResponse(bookingsByStatus.get('failed'))
    }
    return jsonify(result)

@bookings_bp.route('/bookings', methods=['POST'])
def save_booking():
    return save_booking_service(request)

@bookings_bp.route('/bookings/byTicketNo', methods=['GET'])
def get_booking_by_ticket_no():
    ticketId = request.args.get('ticketId')
    if not ticketId:
        return jsonify({"error": "Missing ticketId parameter"}), 400
    return jsonify(getBookingByTicketId(ticketId)), 200



def normalize_place(name):
    return name.lower().replace(" ", "") if name else ""

def parse_date(date_str):
    try:
        if isinstance(date_str, datetime.datetime):
            return date_str
        return parser.parse(date_str)
    except Exception:
        return None

def merge_connected_trips(bookings, status):
    if status == 'upcoming':
        return splitTripsByTime(tripsByPlace(bookings))
    return splitTripsByTime(tripsByPlaceForComplete(bookings))



def tripsByPlace(bookings):
    merged_trips = []
    current_trip = []
    last_dest = None

    for booking in bookings:
        from_loc = normalize_place(booking.get("from"))
        to_loc = normalize_place(booking.get("to"))
        location = normalize_place(booking.get("location"))
        lobName = booking.get("lobName")

        if not current_trip:
            current_trip.append(booking)
            last_dest = to_loc
            continue

        if last_dest:
            if lobName == 'HOTEL' and location == last_dest:
                current_trip.append(booking)
                last_dest = location
                continue
            elif from_loc == last_dest:
                current_trip.append(booking)
                last_dest = to_loc
                continue
            else:
                merged_trips.append(current_trip)
                current_trip = [booking]
                last_dest = location if lobName == 'HOTEL' else to_loc
                continue

    if current_trip:
        merged_trips.append(current_trip)
    return merged_trips


def tripsByPlaceForComplete(bookings):
    merged_trips = []
    current_trip = []
    last_dest = None

    for booking in bookings:
        from_loc = normalize_place(booking.get("from"))
        to_loc = normalize_place(booking.get("to"))
        location = normalize_place(booking.get("location"))
        lobName = booking.get("lobName")

        if not current_trip:
            current_trip.append(booking)
            last_dest = from_loc
            continue

        if last_dest:
            if lobName == 'HOTEL' and location == last_dest:
                current_trip.append(booking)
                last_dest = location
                continue
            elif to_loc == last_dest:
                current_trip.append(booking)
                last_dest = from_loc
                continue
            else:
                merged_trips.append(current_trip)
                current_trip = [booking]
                last_dest = location if lobName == 'HOTEL' else from_loc
                continue

    if current_trip:
        merged_trips.append(current_trip)
    return merged_trips

def splitTripsByTime(tripsByPlace):
    finalTrips = []
    for trip in tripsByPlace:
        finalTrips.append(splittingTripBytime(trip))
    return finalTrips

def splittingTripBytime(bookings):
    merged_trips = []
    current_trip = []
    last_date = None

    for booking in bookings:
        travel_date = parse_date(booking.get("travel_date"))

        if not current_trip:
            current_trip.append(booking)
            last_date = travel_date
            continue

        if last_date and travel_date:
            if abs((travel_date - last_date).days) < 10:
                current_trip.append(booking)
                last_date = travel_date
                continue
            else:
                merged_trips.append(current_trip)
                current_trip = [booking]
                last_date = travel_date
                continue

    if current_trip:
        merged_trips.append(current_trip)
    return merged_trips


def convertToConnectedResponse(bookings):
    result = []
    for booking in bookings or []:
        res_list = []
        res = [booking]
        res_list.append(res)
        result.append(res_list)
    return result