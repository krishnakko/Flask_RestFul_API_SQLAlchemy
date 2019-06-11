from flask_restful import Resource, reqparse
# flask_jwt is jason web token - encoding the data which helps for security reason
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # helps us to get the data in json format easily
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id"
                        )

    @jwt_required()  # tells us we need authorization to access get()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item with name \'{}\' is not found or exists".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name \'{}\' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)  # inserting into ItemModel and creating an object

        try:
            item.save_to_db()  # calling insert method through the item object
        except:
            return {'message': "Error occurred inserting the item "}, 500  # Internal server error
        return item.json(), 201

    @jwt_required()  # tells us we need authorization to access put()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)  # finding an item in database

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']  # What all we want to change or update we can include here

        item.save_to_db()
        return item.json()

    @jwt_required()  # tells us we need authorization  to access delete()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item with name \'{}\' has been deleted'.format(name)}
        return {'message': 'Item with name \'{}\' is not found'.format(name)}


class ItemList(Resource):
    def get(self):
        #  .all() returns all of the objects or data from the data.db
        items = {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return items

