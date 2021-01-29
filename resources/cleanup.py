from flask_restful import Resource
from modules.item import ItemModel
from modules.store import StoreModel
from modules.user import UserModel
from db import db

tables = [ItemModel, StoreModel, UserModel]


class Cleanup(Resource):
    def post(self):
        for table in tables:
            table.query.delete()
        db.session.commit()
        return {"message": "Deleted all tables"}, 201
