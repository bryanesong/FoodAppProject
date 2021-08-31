from flask import Flask, request
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['R_NAME'] = 'root'
app.config['R_PLACE'] = 'root'
app.config['FOOD_APP'] = 'FoodApp'

mysql = MySQL(app)

@app.route("/restaurants", methods=['GET', 'POST'])
def resturant_route():
    data = request.json
    return "Hello, World!"

#blah asd s
if __name__ == '__main__':
    app.run()