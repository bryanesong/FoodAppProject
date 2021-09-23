from typing import Dict
from models.data_models.restaurants_model import Restaurant
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
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        # finds restaurant info

        restInfo1 = YelpFusion().find_restaurant_by_id(id=rest1, headers=headers)
        restInfo2 = YelpFusion().find_restaurant_by_id(id=rest2, headers=headers)

        # test for invalid IDs
        if None == restInfo1 or None == restInfo2:
            return "errorMessage: One or more restaurant IDs are invalid"

        similarity_score = 0
        max_score = 0

        # cuisine, rating, review count, price
        factor_weight = [100, 100, 100, 40, 100]
        for x in range(3, 7):
            temp_similarity_score, temp_max_score = self._compare_CPRR(
                rest1=restInfo1.get_by_index(x),
                rest2=restInfo2.get_by_index(x),
                max_score=factor_weight[x - 3],
            )
            similarity_score += temp_similarity_score
            max_score += temp_max_score
            print(str(temp_similarity_score) + " out of " + str(temp_max_score))
        print(
            "final similarity score: "
            + str(similarity_score)
            + " out of "
            + str(max_score)
            + " max, or "
            + str(round(similarity_score / max_score, 4))
        )

        return str(round(similarity_score / max_score, 4))

    # compare cuisine, price, review count, and rating
    def _compare_CPRR(self, rest1, rest2, max_score: int):
        print(str(rest1) + " compared to " + str(rest2))
        # ensures values are valid
        if (
            None == rest1
            or None == rest2
            or 0 == rest1
            or 0 == rest2
            or rest1 == ""
            or rest2 == ""
        ):
            print("missing restaurant dict info (not fatal)")
            return 0, 0

        # deals with price, review count, and rating
        if (float == type(rest1) == type(rest2)) or (
            str == type(rest1) == type(rest2) or (int == type(rest1) == type(rest2))
        ):
            # rating and review count will be integers. convert $ to integers as well.
            if str == type(rest1) == type(rest2):
                rest1 = len(rest1)
                rest2 = len(rest2)
            # find percent difference
            percent_similar = self._find_percent_similar(rest1, rest2)
            # return score and max score possible
            return max_score * percent_similar, max_score
        # deals with cuisines
        elif list == type(rest1) == type(rest2):
            return self._compare_cuisine_type(
                rest1=rest1, rest2=rest2, max_score=max_score
            )

        # catch all. if rest1 and rest2 types are not the same
        return 0, 0

    def _compare_cuisine_type(self, rest1: dict, rest2: dict, max_score: int):
        # converts dictionary of cuisines to word lists
        cuisine_list1 = self._to_cuisine_list(rest_dict=rest1)
        cuisine_list2 = self._to_cuisine_list(rest_dict=rest2)

        if 0 != len(cuisine_list1) and 0 != len(cuisine_list2):
            # compares words in lists if neither list is empty
            percent_similar = self._compare_cuisine_lists(
                cuisine_list1=cuisine_list1, cuisine_list2=cuisine_list2
            )

            return percent_similar * 100, 100
        else:
            return 0, 0

    def _find_percent_similar(self, num1: float, num2: float):
        percent_similar = num1 / num2
        # flip fraction if percent similar is larger than 1
        if percent_similar > 1:
            percent_similar = 1 / percent_similar
        return percent_similar

    def _to_cuisine_list(self, rest_dict: dict):
        cuisine_list = []
        for cuisine in rest_dict:
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
        # compare every word in word_list1 to every word in word_list2
        for word1 in cuisine_list1:
            w1 = wordnet.synset(word1 + ".n.01")
            for word2 in cuisine_list2:
                print("compared: " + word1 + " and " + word2)
                w2 = wordnet.synset(word2 + ".n.01")
                similarity_score += w1.wup_similarity(w2)
                max_similarity_score += 1
        return (
            (similarity_score / max_similarity_score)
            if max_similarity_score != 0
            else 0
        )
