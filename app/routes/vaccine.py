from flask import Blueprint, request, make_response
import json
from marshmallow import ValidationError
from app import db
from app.models import ApiData
from app.schemas import ReturnVaccine, CreateVaccine
from app import jwt_required

vaccine = Blueprint('vaccine', __name__, url_prefix='/vdata')

"""Get API Data entry by ID"""

@vaccine.route('/<int:id>', methods=['GET'])
@jwt_required
def get_ventry(id, data):
    return_vaccine = ReturnVaccine()
    entry = ApiData.query.filter_by(id=id).first()
    if not entry:
        return make_response(f'ERROR: The requested entry was not found!', 404)
    return {'entry':return_vaccine.dump(entry)}

"""Get API Data entries based on filters"""

@vaccine.route('/', methods=['GET'])
@jwt_required
def get_vdata(data):
    return_vaccine = ReturnVaccine()
    converted_data = []
    data = ApiData.query.all()
    if not data:
        return make_response('ERROR: No entries found in the database!', 404)
    for entry in data:
        converted_data.append(return_vaccine.dump(entry))
    return {'entries': converted_data}

"""Create API Data entry"""

@vaccine.route('/', methods=['POST'])
@jwt_required
def create_ventry(data):
    try:
        return_vaccine = ReturnVaccine()

        """Serialize the data"""
        serialized_entry = CreateVaccine().load(json.loads(request.data))

        print(serialized_entry)

        """Convert data to API Data object"""
        database_entry = ApiData(**serialized_entry)

        """Add entry to database"""
        db.session.add(database_entry)
        db.session.commit()

        return {'entry':return_vaccine.dump(database_entry)}
    
    except (ValidationError) as err:
        return make_response(str(err), 406)
    
"""Update API Data Entry"""    

@vaccine.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required
def update_ventry(id, data):
    try:
      return_vaccine = ReturnVaccine()

      """Serialize the data"""
      serialized_entry = CreateVaccine().load(json.loads(request.data))
      
      """Convert data to API Data object"""
      database_entry = ApiData(**serialized_entry)

      entry = ApiData.query.get(id)
      if not entry:
          return make_response('ERROR: The requested entry was not found!', 404)
      
      """Update entry and add to database"""      
      entry = database_entry
      db.session.commit()

      return {'updated_entry':return_vaccine.dump(entry)}
    
    except ValidationError as err:
        return make_response(str(err), 406)

"""Delete API Data Entry"""

@vaccine.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_ventry(id, data):
    return_vaccine = ReturnVaccine()

    entry = ApiData.query.get(id)
    if not entry:
        return make_response('ERROR: The requested entry was not found!', 404)
      
    """Delete entry from database"""      
    db.session.delete(entry)
    db.session.commit()

    return {'deleted_entry':return_vaccine.dump(entry)}

