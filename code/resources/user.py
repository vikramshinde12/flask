import sqlite3
from flask_restful import Resource, reqparse
from modules.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help="Username should not be blank")
    parser.add_argument('password', required=True, type=str, help="password should not be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"Username {data['username']} already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
