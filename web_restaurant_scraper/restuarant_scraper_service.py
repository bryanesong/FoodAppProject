from models.data_models.restaurants_model import Restaurant
from bs4 import BeautifulSoup
import requests
import json

# DEPRECIATED
class RestaurantWebScraperService:
    def __init__(self):
        pass

    def request_builder(self, zip_code: str, result_pages: int):

        # get link to maps with restaurant search
        url = "https://www.yelp.com/search?cflt=restaurants&find_loc=" + zip_code

        restaurant_count = 0
        current_page = 1
        while current_page <= result_pages:

            # make request to url
            request_result = requests.get(url)
            soup = BeautifulSoup(request_result.text, "html.parser")

            # Build resturant object(name, )
            resturant_name = soup.find_all("a", {"class": "css-166la90"})
            for link in resturant_name:
                name = link.get("name")
                if name is not None:
                    print(restaurant_count, " ", name)
                    print("-----")
                    restaurant_count = restaurant_count + 1

            # # switch to next page for more restaurants based on request and grab new url
            url = (
                "https://www.yelp.com/search?cflt=restaurants&find_loc="
                + zip_code
                + "&start="
                + str(current_page * 10)
            )

            current_page = current_page + 1

        # will parse html response from google search to find link leading to maps link

        # use link to perform another web scrape for more information

        # located in class "eZt8xd"
        # for link in soup.find_all('a'):
        #     if 'maps.google.com/maps' in link.get('href'):
        #         print(count)
        #         print(link.get('href'))
        #         print("------")
        #     count = count+1

        # temp = soup.find("a" , class_='tiS4rf Q2MMlc')

        # print(temp)
        # tiS4rf Q2MMlc
