from time import sleep

from flask import Blueprint, jsonify, request
from services.flight_service import (
    generate_flight, group_by_flight, get_flights_from_file, get_flights_from_db, get_fare_categories
)
from vendors.mongo_client import amadeus_collection, convert_object_id
import random

flights_bp = Blueprint('flights', __name__)

@flights_bp.route('/', methods=['GET'])
def get_flights():
    flights = [generate_flight(i) for i in range(3000)]
    for flight in flights:
        flight['fareCategories'] = get_fare_categories(flight['price'])
    amadeus_collection.insert_many(flights)
    return jsonify([convert_object_id(doc) for doc in flights])

@flights_bp.route('/paginated', methods=['GET'])
def get_flights_paginated():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))
    return get_flights_from_file(page, per_page)

@flights_bp.route('/search', methods=['GET'])
def search_flights():
    sleep(1)
    source = request.args.get('from')
    destination = request.args.get('to')
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('size', 20)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    if not source or not destination:
        return jsonify({"error": "Missing 'from' or 'to' parameter"}), 400
    flights = get_flights_from_db(source, destination, start*end, end)
    return jsonify({
        "page": page,
        "perPage": per_page,
        "current_count": len(flights),
        "flights": flights
    })