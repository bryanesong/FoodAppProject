from flask import request, render_template, make_response, abort, Response
from datetime import datetime as dt
from flask import current_app as app
from models.sql_models.user_model import User
from services.restaurants.restaurant_service import RestaurantService
from services.user_accounts.user_account_service import UserAccountService
from services.restaurants.restaurant_comparer import RestaurantComparer

# this will only retrieve food places that are currently OPEN
@app.route("/restaurants", methods=["GET", "POST"])
def resturant_route():
    lat = request.args.get("lat")
    long = request.args.get("long")
    num_results = request.args.get("num_results")
    # 47.5855941
    # -122.0690723

    return RestaurantService().get_restaurant_in_area(
        lat=lat, long=long, num_results=num_results
    )


@app.route("/users", methods=["POST"])
def create_user():
    uuid = request.args.get("uuid")
    username = request.args.get("username")
    email = request.args.get("email")

    if uuid is None or username is None or email is None:
        return Response(
            "{'errorMessage': 'uuid, username, or email is invalid.'}", status=400
        )

    return UserAccountService().create_user_account(uuid, username, email)


# compares 2 restaurants
@app.route("/restaurants/compare", methods=["GET"])
def compare_route():
    # test for missing IDs
    if None != request.args.get("rest1") and None != request.args.get("rest2"):
        rest1 = request.args.get("rest1")
        rest2 = request.args.get("rest2")
        return RestaurantComparer().compare_restaurants(rest1=rest1, rest2=rest2)

    else:
        return "errorMessage: One or more restaurant IDs are missing"


@app.route("/users", methods=["GET"])
def get_all_users():
    return UserAccountService().get_all_users()
