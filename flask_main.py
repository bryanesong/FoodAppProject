from flask import Flask, request
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow
from services.restaurants.restaurant_service import RestaurantService

app = Flask(__name__)


# this will only retrieve food places that are currently OPEN
@app.route("/restaurants", methods=['GET', 'POST'])
def resturant_route():
    lat = request.args.get('lat')
    long = request.args.get('long')
    num_results = request.args.get('num_results')
    # 47.5855941
    # -122.0690723

    return RestaurantService().get_restaurant_in_area(lat=lat, long=long,num_results=num_results)

#yeet
if __name__ == '__main__':
    app.run()