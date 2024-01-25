from flask import Blueprint, request, make_response
import json

from marshmallow import ValidationError
from app import db
from app.models import ScrapeData
from app.schemas import CreateScrape, ReturnScrape

create_scrape = CreateScrape()
return_scrape = ReturnScrape()

scrape = Blueprint('scrape', __name__, url_prefix='/sdata')

"""Get API Data entry by ID"""

@scrape.route('/<int:id>', methods=['GET'])
def get_sentry(id):
    entry = ScrapeData.query.filter_by(id=id).first()
    if not entry:
        return make_response(f'ERROR: The requested entry was not found!', 404)
    return {'entry':return_scrape.dump(entry)}

"""Get API Data entries based on filters"""

@scrape.route('/', methods=['GET'])
def get_sdata():
    converted_data = []
    data = ScrapeData.query.all()
    if not data:
        return make_response('ERROR: No entries found in the database!', 404)
    for entry in data:
        converted_data.append(return_scrape.dump(entry))
    return {'entries': converted_data}

"""Create API Data entry"""

@scrape.route('/', methods=['POST'])
def create_sentry():
    try:

        """Serialize the data"""
        serialized_entry = CreateScrape().load(json.loads(request.data))

        print(serialized_entry)

        """Convert data to API Data object"""
        database_entry = ScrapeData(**serialized_entry)

        """Add entry to database"""
        db.session.add(database_entry)
        db.session.commit()

        return {'entry':return_scrape.dump(database_entry)}
    
    except (ValidationError) as err:
        return make_response(str(err), 406)
    
"""Update API Data Entry"""    

@scrape.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_sentry(id):
    try:
      
      """Serialize the data"""
      serialized_entry = CreateScrape().load(json.loads(request.data))
      
      """Convert data to API Data object"""
      database_entry = ScrapeData(**serialized_entry)

      entry = ScrapeData.query.get(id)
      if not entry:
          return make_response('ERROR: The requested entry was not found!', 404)
      
      """Update entry and add to database"""      
      entry = database_entry
      db.session.commit()

      return {'updated_entry':return_scrape.dump(entry)}
    
    except ValidationError as err:
        return make_response(str(err), 406)

"""Delete API Data Entry"""

@scrape.route('/<int:id>', methods=['DELETE'])
def delete_sentry(id):
    entry = ScrapeData.query.get(id)
    if not entry:
        return make_response('ERROR: The requested entry was not found!', 404)
      
    """Delete entry from database"""      
    db.session.delete(entry)
    db.session.commit()

    return {'deleted_entry':return_scrape.dump(entry)}