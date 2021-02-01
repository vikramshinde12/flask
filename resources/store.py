from flask_restful import Resource
from modules.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store Not Found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A Store {name} already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating the store"}, 500

        return {"message": f"The Store {name} added successfully."}

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        else:
            return {"message": "Store does not exists"}, 400

        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
