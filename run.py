from app import app
from db import db

db.init_app(app)


@app.before_first_request  # It will run before any request executes
def create_tables():
    db.create_all()  # It will create all the tables in data.db

