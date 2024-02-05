from flask import request, make_response
from flask.views import MethodView
import json
from marshmallow import ValidationError
from app import db
from flask_smorest import Blueprint, abort
from app.models import ScrapeData
from app import jwt_required
from app.schemas import CreateScrape, ReturnScrape, QueryArgsSchema, AggQueryArgsSchema
from sqlalchemy import func, TIMESTAMP, cast


create_scrape = CreateScrape()
return_scrape = ReturnScrape()

scrape = Blueprint('Scraped Vaccine Data', __name__, url_prefix='/sdata', description="Endpoints to manipulate data scraped from the CDC's website.")

"""Get Scrape Data entry by ID"""

@scrape.route('/<int:id>')

class get_sentry(MethodView):
    @jwt_required
    def get(self, id, data):
        entry = ScrapeData.query.filter_by(id=id).first()
        if not entry:
            return make_response(f'ERROR: The requested entry was not found!', 404)
        return {'entry':return_scrape.dump(entry)}

"""Get Scrape Data entries based on filters"""

@scrape.route('/')
class get_sdata(MethodView):
    @scrape.arguments(QueryArgsSchema, location="query")
    def get(self, args):
        converted_data = []
        print(args)
        data = ScrapeData.query.filter_by(**args).order_by(ScrapeData.date).all()
        if not data:
            return make_response('ERROR: No entries found in the database!', 404)
        for entry in data:
            converted_data.append(return_scrape.dump(entry))
        return {'entries': converted_data}
    
"""Create Scrape Data entry"""

@scrape.route('/')
class create_sentry(MethodView):
    @jwt_required
    def post(self, data):
        try:

            """Serialize the data"""
            serialized_entry = CreateScrape().load(json.loads(request.data))


            """Convert data to API Data object"""
            database_entry = ScrapeData(**serialized_entry, user_id=data['user_id'])

            """Add entry to database"""
            db.session.add(database_entry)
            db.session.commit()

            return {'entry':return_scrape.dump(database_entry)}
        
        except (ValidationError) as err:
            return make_response(str(err), 406)
    
"""Update Scrape Data Entry"""    

@scrape.route('/<int:id>')

class update_sentry(MethodView):
    @jwt_required
    def put(self, id, data):
        try:
        
            """Serialize the data"""
            serialized_entry = CreateScrape().load(json.loads(request.data))
            
            """Convert data to API Data object"""
            database_entry = ScrapeData(**serialized_entry)

            entry = ScrapeData.query.get(id)
            if not entry:
                return make_response('ERROR: The requested entry was not found!', 404)
            
            if entry.user_id != int(data['user_id']):
                return make_response("ERROR: Cannot update another user's entry!", 403)

            
            """Update entry and add to database"""      
            entry = database_entry
            db.session.commit()

            return {'updated_entry':return_scrape.dump(entry)}
        
        except ValidationError as err:
            return make_response(str(err), 406)

"""Delete Scrape Data Entry"""

@scrape.route('/<int:id>')

class delete_sentry(MethodView):
    @jwt_required
    def delete(self, id, data):
        entry = ScrapeData.query.get(id)
        if not entry:
            return make_response('ERROR: The requested entry was not found!', 404)
        
        if entry.user_id != int(data['user_id']):
                return make_response("ERROR: Cannot delete another user's entry!", 403)
        
        """Delete entry from database"""      
        db.session.delete(entry)
        db.session.commit()

        return {'deleted_entry':return_scrape.dump(entry)}