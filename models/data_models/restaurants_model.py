class Restaurant:

    def __init__(self, id, name, cusine, rating, image_url):
        self.id = id 
        self.name = name
        self.cusine = cusine
        self.rating = rating
        self.image_url = image_url
    
    def toDict(self) -> dict:
        temp = {}
        temp['id'] = self.id
        temp['name'] = self.name
        temp['cusine'] = self.cusine
        temp['rating'] = self.rating
        temp['image_url'] = self.image_url
        return temp 
    