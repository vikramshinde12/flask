from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

# from security import authenticate, identity
from resources.user import UserRegister, User, \
    UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.cleanup import Cleanup
from blacklist import BLACKLIST
from db import db

app = Flask(__name__)
# app.secret_key = 'jose'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@34.89.38.19:3306/api'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@/api?unix_socket=/cloudsql/flask-demo-11:europe-west2:store"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['PROPAGATE_EXCEPTION'] = True #propogate the jwt-exception
app.config['JWT_SECRET_KEY'] = 'vikramshinde-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)
api = Api(app)

# jwt = JWT(app, authenticate, identity) # generates /auth automatically
jwt = JWTManager(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# @app.after_request
# def after_request():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response


@jwt.user_claims_loader
def add_identity_to_claims(identity):
    if identity == 1: #Instead of hard coding, read from config file or database.
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token expired'
    }), 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # return decrypted_token['identity'] in BLACKLIST
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Cleanup, '/cleanup')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=8080)
