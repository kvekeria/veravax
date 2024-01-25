from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

ma = Marshmallow(app)

from app.routes import vaccine, scrape

app.register_blueprint(vaccine.vaccine)
app.register_blueprint(scrape.scrape)

@app.route('/')
def home():
    return render_template('index.html', title='Home - VeraVax API')

