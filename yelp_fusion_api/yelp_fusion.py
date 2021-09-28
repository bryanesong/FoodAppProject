from models.data_models.restaurants_model import Restaurant
import requests
from constants import API_TOKEN
import json


class YelpFusion:
    def __init__(self):
        pass

    def get_restaurants_in_area(self, lat, long, results):
        url = f"https://api.yelp.com/v3/businesses/search?term=food&latitude={lat}&longitude={long}&limit={results}&open_now=True"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        response = requests.get(url, headers=headers)

        res = response.text
        print(res)

        # convert to json
        res_as_json = json.loads(res)

        # test if no nearby businesses are found
        if not "businesses" in res_as_json.keys():
            return "errorMessage: no nearby businesses found"
        food_places = res_as_json["businesses"]

        # build list of resturant objects
        food_place_id_list = []
        # food_place_prices = []

        for place in food_places:
            print(place["name"], " - ", place["id"])
            print("-----")
            food_place_id_list.append(place["id"])
            # food_place_prices.append(len(place['price']))

        restaurant_list = []
        current_food_item = 0
        # make calls to each id on the list to get detailed information
        for food_place_id in food_place_id_list:
            # iterate counter for restaurant pricing
            current_food_item = current_food_item + 1
            # restaurant_list.append(Restaurant(place['name'],len(place['price']), ))#name, price, cuisine, rating)
            # print(response.status_code)
            print(food_place_id)
            restaurant_list.append(
                self.find_restaurant_by_id(id=food_place_id, headers=headers)
            )

        return restaurant_list

    def find_restaurant_by_id(self, id: str, headers: dict):
        url = "https://api.yelp.com/v3/businesses/" + id

        # request utlizes same header as before because of same auth token
        response = requests.get(url, headers=headers)

        # convert to json
        res = response.text
        current_res = json.loads(res)
        # test for invalid ID
        if "id" in current_res.keys():
            return Restaurant(
                current_res["id"],
                current_res["name"],
                current_res["categories"],
                current_res["rating"],
                current_res["image_url"],
                current_res["review_count"],
                current_res["price"] if "price" in current_res.keys() else "",
            )
        else:
            return "errorMessage: Invalid restaurant ID"
