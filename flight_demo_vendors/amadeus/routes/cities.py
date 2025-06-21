from flask import Blueprint, jsonify, request
from flight_demo_vendors.amadeus.services.city_service import search_cities_by_keyword_service

cities_bp = Blueprint('cities', __name__)

@cities_bp.route('/search', methods=['GET'])
def search_cities():
    keyword = request.args.get('keyword')
    if not keyword or len(keyword) <= 2:
        return jsonify({"error": "Parameter 'keyword' is required and must be at least 3 characters long."}), 400
    from_param = request.args.get('from')
    cities = search_cities_by_keyword_service(keyword, from_param)
    return jsonify({"cities": cities})