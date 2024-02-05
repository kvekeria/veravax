import jwt
import json
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request, make_response, jsonify, flash, render_template, url_for, redirect
from werkzeug.security import check_password_hash
from app.schemas import LoginUser
from app import app
from app.forms import LoginForm
from app.models import User

login = Blueprint('Authentication', __name__, url_prefix='/login', description='Endpoint to login user into system using JWT tokens.')
    
@login.route('/')
class login_user(MethodView):
    @login.arguments(LoginUser)
    def post(self, credentials):
        email = credentials['email']
        password = credentials['password']
        user = User.query.filter_by(email=email).first()
        
        if user == None:
            return make_response('ERROR: Requested User Not Found!', 404)
        
        if not check_password_hash(user.password, password):
            return make_response('ERROR: Password incorrect!', 401)
        
        """Generate token"""
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify(access_token=token), 200