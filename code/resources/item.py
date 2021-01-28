from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from modules.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store id.")

    @jwt_required()
    def get(self, name):
            item = ItemModel.find_by_name(name)

            if item:
                return item.json(), 200
            else:
                return {"message": "Not Found"}, 404

    def post(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"item {name} already exists"}, 400

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if not item:
            return {"message": f"item {name} does not exists"}, 404
        else:
            item.delete_from_db()

        return {"message": "Item deleted"}, 204

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json(), 204


class ItemList(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {"items": items}, 200
