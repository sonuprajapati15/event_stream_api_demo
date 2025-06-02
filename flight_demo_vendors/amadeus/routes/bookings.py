from flask import Blueprint, jsonify, request
from services.booking_service import get_all_bookings_service, save_booking_service, getBookingByTicketId

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def get_bookings_by_route():
    userid = request.args.get('userId')
    if not userid:
        return jsonify({"error": "Missing userid parameter"}), 400
    return jsonify(get_all_bookings_service(userid))

@bookings_bp.route('/bookings', methods=['POST'])
def save_booking():
    return save_booking_service(request)

@bookings_bp.route('/bookings/byTicketNo', methods=['GET'])
def get_booking_by_ticket_no():
    ticketId = request.args.get('ticketId')
    if not ticketId:
        return jsonify({"error": "Missing ticketId parameter"}), 400
    return jsonify(getBookingByTicketId(ticketId)), 200