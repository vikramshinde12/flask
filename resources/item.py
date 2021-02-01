from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required, current_identity
from flask_jwt_extended import jwt_required, get_jwt_claims, \
    jwt_optional, get_jwt_identity, fresh_jwt_required
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

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        else:
            return {"message": "Not Found"}, 404

    @fresh_jwt_required
    def post(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"item {name} already exists"}, 400

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except ValueError:
            return {"message": "Some value is incorrect"}, 400
        except Exception:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
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
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json(), 204


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        print(user_id)
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {'items': [item['name'] for item in items],
                'message': 'More data available if you log in.'
                }, 200
