import jwt
from flask import request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import app
from datetime import datetime

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return make_response('ERROR: Token required!', 401)
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return make_response('ERROR: Token has expired!', 401)
        except jwt.InvalidTokenError:
            return make_response('ERROR: Invalid token!', 401)
        
        return f(data, *args, **kwargs)
    return wrapper
    
