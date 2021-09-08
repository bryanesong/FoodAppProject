class Restaurant:

    def __init__(self, id, name, cuisine, rating, image_url, review_count, price):
        self.id = id 
        self.name = name
        self.cuisine = cuisine
        self.rating = rating
        self.image_url = image_url
        self.review_count = review_count
        self.price = price
    
    def toDict(self) -> dict:
        temp = {}
        temp['id'] = self.id
        temp['name'] = self.name
        temp['cuisine'] = self.cuisine
        temp['rating'] = self.rating
        temp['image_url'] = self.image_url
        temp['review_count'] = self.review_count
        temp['price'] = self.price
        return temp 
    