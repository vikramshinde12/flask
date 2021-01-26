import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        user = current_identity
        print(f'current user {user}')
        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        print(row)

        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200
        else:
            return {"message": "Not Found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        print(row)

        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def post(self, name):

        if self.find_by_name(name):
            return {"message": f"item {name} already exists"}, 400

        data = Item.parser.parse_args()

        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500


        return item, 201

    def delete(self, name):

        if not self.find_by_name(name):
            return {"message": f"item {name} does not exists"}, 404

        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()
        insert_query = "DELETE FROM items WHERE name=?"
        cursor.execute(insert_query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}, 204

    def put(self, name):

        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured at insert"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured at update"}, 500
        return updated_item, 204

    @classmethod
    def update(cls, item):
        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()
        insert_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(insert_query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.Connection('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"

        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            item = {'name': row[0], 'price': row[1]}
            items.append(item)

        return {"items": items}, 200
