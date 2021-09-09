from flask import Flask, request, render_template
from services.restaurants.restaurant_comparer import RestaurantComparer
from flask import Flask, request
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    db.init_app(app)

    with app.app_context():
        import routes.routes  # import routes

        db.create_all()  # Create database tables for our data models

        return app
