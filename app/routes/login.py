from flask import Blueprint, request
from app.schemas import LoginUser
from app import guard
import json

login = Blueprint('login', __name__, url_prefix='/login')

@login.route('/', methods=['POST'])
def login():
    serialized_entry = LoginUser().load(json.loads(request.data))
    guard.authenticate(serialized_entry.username, serialized_entry.password)

