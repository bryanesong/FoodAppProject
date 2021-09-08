from typing import Dict
from models.restaurants_model import Restaurant
from constants import API_TOKEN
from yelp_fusion_api.yelp_fusion import YelpFusion
import nltk
from nltk.corpus import wordnet
import re

class RestaurantComparer:

    def __init__(self):
        self.curr_resturant = None

    def compare_restaurants(self, rest1, rest2):
        # takes in restaurant 1 id & restaurant 2 id
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }
        # finds restaurant info
        restInfo1 = YelpFusion().find_restaurant_by_id(id=rest1, headers=headers)
        restInfo2 = YelpFusion().find_restaurant_by_id(id=rest2, headers=headers)

        similarity_score = 0
        max_score = 0

        # compares price, number of reviews, rating, and cuisine type
        temp_similarity_score, temp_max_score = self._compare_price(rest1 = restInfo1, rest2 = restInfo2)
        similarity_score += temp_similarity_score
        max_score += temp_max_score
        print("similarity score: " + str(temp_similarity_score) + " max score: " + str(temp_max_score))

        temp_similarity_score, temp_max_score = self._compare_review_count(rest1 = restInfo1, rest2 = restInfo2)
        similarity_score += temp_similarity_score
        max_score += temp_max_score
        print("similarity score: " + str(temp_similarity_score) + " max score: " + str(temp_max_score))

        temp_similarity_score, temp_max_score = self._compare_rating(rest1 = restInfo1, rest2 = restInfo2)
        similarity_score += temp_similarity_score
        max_score += temp_max_score
        print("similarity score: " + str(temp_similarity_score) + " max score: " + str(temp_max_score))

        temp_similarity_score, temp_max_score = self._compare_cuisine_type(rest1 = restInfo1, rest2 = restInfo2)
        similarity_score += temp_similarity_score
        max_score += temp_max_score
        print("similarity score: " + str(temp_similarity_score) + " max score: " + str(temp_max_score))

        return str(similarity_score/max_score)

    def _compare_price(self, rest1: Restaurant, rest2: Restaurant):
        max_score = 100
        # price difference range is 0-3
        price_difference = abs(len(rest1.price) - len(rest2.price))
        if "" != rest1.price and rest2.price:
            print("price 1: " + rest1.price + " price 2: " + rest2.price)
            # return score and max score possible
            return max_score - (33 * price_difference), max_score
        else:
            # if unable to factor in price, return a score of 0 and a max score of 0
            return 0, 0

    def _compare_review_count(self, rest1: Restaurant, rest2: Restaurant):
        max_score = 20
        
        # ensure restaurant has been rated
        if 0 != rest1.review_count and rest2.review_count:
            print("review count 1: " + str(rest1.review_count) + " review count 2: " + str(rest2.review_count))
            # review count similarity will be based on percent similarity
            percent_similar = self._find_percent_similar(rest1.review_count, rest2.review_count)
            return max_score * percent_similar, max_score

        else:
            return 0, 0
    
    def _compare_rating(self, rest1: Restaurant, rest2: Restaurant):
        max_score = 100
        
        # ensure restaurant has been rated
        if 0 != rest1.rating and rest2.rating:
            print("rating 1: " + str(rest1.rating) + " rating 2: " + str(rest2.rating))
            # rating similarity will be based on percent similarity
            percent_similar = self._find_percent_similar(rest1.rating, rest2.rating)
            return max_score * percent_similar, max_score

        else:
            return 0, 0

    def _compare_cuisine_type(self, rest1: Restaurant, rest2: Restaurant):
        max_score = 100

        #converts dictionary of cuisines to word lists
        cuisine_list1 = self._to_cuisine_list(restaurant=rest1)
        cuisine_list2 = self._to_cuisine_list(restaurant=rest2)

        if 0 is not len(cuisine_list1) and len(cuisine_list2):
            # compares words in lists if neither list is empty
            percent_similar = self._compare_cuisine_lists(cuisine_list1 = cuisine_list1, cuisine_list2 = cuisine_list2)

            return percent_similar * 100, 100
        else:
            return 0, 0

    
    def _find_percent_similar(self, num1: float, num2: float):
        percent_similar = num1/num2
            # flip fraction if percent similar is larger than 1
        if percent_similar > 1:
            percent_similar = 1/percent_similar
        return percent_similar

    def _to_cuisine_list(self, restaurant: Restaurant):
        cuisine_list = []
        for cuisine in restaurant.cuisine:
            cuisine_list + re.split(" |/", cuisine["alias"])
            cuisine_list.append(cuisine["alias"])
        print(cuisine_list)
        return self._remove_invalids(cuisine_list)
    
    def _remove_invalids(self, word_list: Dict):
        new_word_list = []
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        # add current word to new_word_list if exists in vocab list
        for word in word_list:
            if word in english_vocab:
                new_word_list.append(word)
            # remove last letter (hopefully an s) and test again
            elif word[0:-1] in english_vocab:
                new_word_list.append(word[0:-1])
        print(new_word_list)
        return new_word_list

    def _compare_cuisine_lists(self, cuisine_list1: list, cuisine_list2: list):
        similarity_score = 0
        max_similarity_score = 0
        #compare every word in word_list1 to every word in word_list2
        for word1 in cuisine_list1:
            w1 = wordnet.synset(word1 + ".n.01")
            for word2 in cuisine_list2:
                print("compared: " + word1 + " and " + word2)
                w2 = wordnet.synset(word2 + ".n.01")
                similarity_score += w1.wup_similarity(w2)
                max_similarity_score += 1
        return (similarity_score/max_similarity_score) if max_similarity_score is not 0 else 0

