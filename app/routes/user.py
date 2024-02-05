from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import json
from app.schemas import CreateUser, ReturnUser
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from app import jwt_required, db
from app.models import User

user = Blueprint('Users', 'user', url_prefix='/users', description='Endpoints to manipulate stored users.')

@user.route('/')
class create_user(MethodView):
    @user.arguments(CreateUser)
    @user.response(201, ReturnUser)
    def post(self, new_user):
        try:
            """Serialize entry"""
            if User.query.filter_by(email=new_user['email']).first():
                abort(401,'User already exists!')
            database_entry = User(email=new_user['email'], password=generate_password_hash(new_user['password'], method="scrypt:32768:8:1"))  
            db.session.add(database_entry)
            db.session.commit()
            return database_entry
        except ValidationError:
            abort(401,'ERROR: Invalid email address!')
    

@user.route('/')
@jwt_required
class update_user(MethodView):
    @user.arguments(CreateUser)
    @user.response(201, ReturnUser)
    def put(self, updated_user):
        try:
            database_entry = User(email=updated_user['email'], password=generate_password_hash(updated_user['password'], "sha256"))
            database_user = User.query.filter_by(email=updated_user['email']).first()
            if not database_user:
                abort(404,'ERROR: User not found!')
            database_user = user
            db.commit()
            return database_entry
        except ValidationError:
            abort(404,'ERROR: Invalid email address!')
            

@user.route('/<int:id>')
@jwt_required
class delete_user(MethodView):
    @user.response(201, ReturnUser)
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404,'ERROR: User not found!')
        db.session.delete(user)
        db.session.commit()
        return user





