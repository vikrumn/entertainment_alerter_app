from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
#from resources.item import Item, ItemList #Importing here lets sqlalchemy know what tables exist
#from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost:5432/postgres' # can be mysql, postgresql, others
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vik'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()
	

jwt = JWT(app, authenticate, identity) #creates new endpoint, /auth
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug = True)
