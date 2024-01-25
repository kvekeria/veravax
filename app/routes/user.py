from flask import Blueprint, request
from app import guard, db
from app.schemas import CreateUser
from marshmallow import ValidationError
from app.models import User
import json

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['POST'])
def add_user():
    try:
        """Serialize the data"""
        serialized_entry = CreateUser().load(json.loads(request.data))

        print(serialized_entry)

        """Convert data to API Data object"""
        database_entry = User(**serialized_entry)

        """Add user to database"""
        db.session.add(database_entry)
        db.session.commit()

    except ValidationError as err:
        return {"user":""}