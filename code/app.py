from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.secret_key = 'jose'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

@app.before_first_request
def create_table():
    db.create_all()


api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


@jwt.jwt_error_handler
def customised_error_handler(error):
    print('I am in error handler..')
    return jsonify({
        "message": error.description,
        "code": error.status_code
    }), error.status_code


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
