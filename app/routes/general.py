from flask import render_template, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from app.forms import LoginForm
import json
import subprocess

general = Blueprint('General', 'general', description='General endpoints for the rendering of UI elements.')

@general.route('/')
class home(MethodView):
    def get(self):
        return render_template('index.html', title='Home - veravax API')

@general.route('/viewdata')
class view_data(MethodView):
    def get(self):
        return render_template('view-data.html', title='View Data - veravax API')

# @general.route('/getadata')
# def get_api_data():
#     # Run api_engine.py using subprocess
#     subprocess.run(['python', 'api_engine.py'])
#     return jsonify({"message": "API data retrieval initiated."})

# @general.route('/getsdata')
# def get_scrape_data():
#     # Run janssen_scrapper.py using subprocess
#     subprocess.run(['python', 'janssen_scraper.py'])
#     return jsonify({"message": "Scrape data retrieval initiated."})
    
# @general.route('/docs/')
# class redoc(MethodView):
#     def get(self):
#         return render_template('redoc.html', redoc_url='/api/spec')


