from models.data_models.restaurants_model import Restaurant
from services.restaurants.restaurant_comparer import RestaurantComparer
from yelp_fusion_api.yelp_fusion import YelpFusion
from services.restaurants.restaurant_service import RestaurantService
from constants import API_TOKEN


class RestaurantFindCompare:
    def __init__(self) -> None:
        pass

    # pre: takes in lattitude, longitude, and restaurant ID
    # assumes lat and long are non null, and restaurant is a valid ID
    # returns "no nearby businesses" if no businesses are found
    # post: returns a dictionary of restaurants ordered from least comparable to most comparable, with scores as keys
    def find_and_compare(self, lat: float, long: float, restaurant: str):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        # retrieve info of liked restaurant
        liked_restaurant = YelpFusion().find_restaurant_by_id(
            id=restaurant, headers=headers
        )
        if liked_restaurant != None:
            # retrieve list of nearbly restaurants
            nearby_restaurants = RestaurantService().get_restaurant_in_area(
                lat=lat, long=long, num_results=10, serialize=False
            )
            # if error message is returned, return again
            if type(nearby_restaurants) == str:
                return nearby_restaurants

            # list of scores
            score_list = []

            # populate score_list with numbers
            for restaurant in nearby_restaurants:
                score_list.append(
                    RestaurantComparer().compute_scores(
                        restInfo1=restaurant, restInfo2=liked_restaurant
                    )
                )

            for i in range(len(nearby_restaurants)):
                highest_score = 0
                index_of_high_score = -1
                for j in range(i, len(nearby_restaurants)):
                    if score_list[j] > highest_score:
                        highest_score = score_list[j]
                        index_of_high_score = j
                # set temp values
                temp_score = score_list[i]
                temp_restaurant = nearby_restaurants[i]
                # swap scores
                score_list[i] = score_list[index_of_high_score]
                score_list[index_of_high_score] = temp_score
                # swap restaurants
                nearby_restaurants[i] = nearby_restaurants[index_of_high_score]
                nearby_restaurants[index_of_high_score] = temp_restaurant

            return self._combine_restaurant_with_scores(
                restaurant_list=nearby_restaurants, score_list=score_list
            )

        else:
            return "errorMessage: invalid restaurant id for find_and_compare route"

    # combines restaurants with respective scores
    def _combine_restaurant_with_scores(
        self, restaurant_list: list[Restaurant], score_list: list[int]
    ):
        combined_dict = {}
        for index, restaurant in enumerate(restaurant_list):
            combined_dict[score_list[index]] = restaurant.toDict()
        return combined_dict
