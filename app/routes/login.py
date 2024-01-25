import jwt
import json
from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import check_password_hash
from app.schemas import LoginUser
from app import app
from app.models import User

login = Blueprint('login', __name__, url_prefix='/login')

@login.route('/', methods=['POST'])
def login_user():

    """Serialize Login"""
    login_data = LoginUser().load(json.loads(request.data))

    email = login_data["email"]
    password = login_data['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        return make_response('ERROR: Requested user not found!', 404)
    
    if not check_password_hash(user.password, password):
        return make_response('ERROR: Password incorrect!', 401)
    
    """Generate token"""
    token = jwt.encode({'email': user['email']}, app.config['SECRET_KEY'])
    return jsonify(access_token=token.decode('UTF-8')), 200