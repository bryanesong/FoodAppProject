from yelp_fusion_api.yelp_fusion import YelpFusion
from models.restaurants_model import Restaurant
from web_restaurant_scraper.restuarant_scraper_service import RestaurantWebScraperService

class RestaurantService:

    def __init__(self):
        self.curr_resturant = None

    #takes in lat/long, radius(miles)
    def get_restaurant_in_area(self, lat, long, num_results):
       return self._serialize_get_restaurants(YelpFusion().get_restaurants_in_area(lat, long, num_results))

    def _serialize_get_restaurants(self, restaurants_list: list[Restaurant]):
        counter = 0
        temp = {}
        for restaurant in restaurants_list:
            temp[counter] = restaurant.toDict()
            counter = counter+1
        return temp

    