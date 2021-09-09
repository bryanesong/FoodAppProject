class Restaurant:

    def __init__(self, id, name, cuisine, rating, image_url, review_count, price):
        self.id = id 
        self.image_url = image_url
        self.name = name
        self.cuisine = cuisine
        self.rating = rating
        self.review_count = review_count
        self.price = price
    
    def toDict(self) -> dict:
        temp = {}
        temp['id'] = self.id
        temp['image_url'] = self.image_url
        temp['name'] = self.name
        temp['cuisine'] = self.cuisine
        temp['rating'] = self.rating
        temp['review_count'] = self.review_count
        temp['price'] = self.price
        return temp
    
    def get_by_index(self, index: int):
        dict = self.toDict()
        key_list = list(dict.keys())
        # returns value based on index
        if len(key_list) > index:
            return dict[key_list[index]]
        else:
            print("index out of bounds")
            return None
    