from flask import Blueprint, request, make_response
import json
from app.schemas import CreateUser, ReturnUser
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from app import jwt_required
from app.models import User
from app import db

user = Blueprint('user', __name__, url_prefix='/users')

@user.route('/', methods=['POST'])
def create_user():
    try:
        return_user = ReturnUser()
        """Serialize entry"""
        user = CreateUser().load(json.loads(request.data))
        if User.query.filter_by(email=user['email']).first():
            return make_response('User already exists!', 401)
        database_entry = User(email=user['email'], password=generate_password_hash(user['password'], method="scrypt:32768:8:1"))  
        db.session.add(database_entry)
        db.session.commit()
        return {'user':return_user.dump(database_entry)}
    except ValidationError:
        return make_response('ERROR: Invalid email address!', 401)
    
@user.route('/', methods=['PUT', 'PATCH'])
@jwt_required
def update_user(data):
    try:
        user = CreateUser().load(json.loads(request.data))
        database_entry = User(email=user['email'], password=generate_password_hash(user['password'], "sha256"))
        database_user = User.query.filter_by(email=data['email']).first()
        if not database_user:
            return make_response('ERROR: User not found!', 404)
        database_user = user
        db.commit()
        return {'updated_user':ReturnUser().dump(database_entry)}
    except ValidationError:
        return make_response('ERROR: Invalid email address!', 401)



@user.route('/', methods=["DELETE"])
@jwt_required
def delete_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        make_response('ERROR: User not found!', 404)
    db.session.delete(user)
    db.session.commit()
    return {'deleted_user', ReturnUser().dump(user)}





