import os
from flask import Flask
from flask_restful import Api

# flask_jwt is jason web token - encoding the data which helps for security reason
from flask_jwt import JWT
# secret key helps to secure data
from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # sql database will s
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'krishna'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # going to app, authenticates , identity together to allow for authentication
# of users

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
