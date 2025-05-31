from flask import Flask
from routes.flights import flights_bp
from routes.bookings import bookings_bp
from routes.cities import cities_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(flights_bp, url_prefix='/amadeus/api/flights')
app.register_blueprint(bookings_bp, url_prefix='/amadeus/api/v1')
app.register_blueprint(cities_bp, url_prefix='/amadeus/api/cities')

if __name__ == '__main__':
    app.run(debug=True, port=5000)