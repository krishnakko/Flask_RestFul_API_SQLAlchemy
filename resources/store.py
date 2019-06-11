from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'Message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store with the name \'{}\' already exists'.format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'Message': 'An error occurred creating the store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'Message': 'Store with name \'{}\' is successfully deleted.'.format(name)}
        return {'Message': 'The Store with name \'{}\' is not found.'.format(name)}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}
