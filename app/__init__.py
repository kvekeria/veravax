from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_smorest import Api, Blueprint, abort

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

ma = Marshmallow(app)

from app.oauth import jwt_required

api = Api(app)

from app.routes import general, vaccine, user, login, scrape

api.register_blueprint(general.general)
api.register_blueprint(vaccine.vaccine)
api.register_blueprint(user.user)
api.register_blueprint(scrape.scrape)
api.register_blueprint(login.login)

# api.spec_path = '/api/spec'

