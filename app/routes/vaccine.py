from flask import Blueprint, request, make_response
import json
from marshmallow import ValidationError
from app import db, guard, flask_praetorian
from app.models import ApiData
from app.schemas import ReturnVaccine, CreateVaccine

vaccine = Blueprint('vaccine', __name__, url_prefix='/vdata')

"""Get API Data entry by ID"""

@flask_praetorian.auth_required
@vaccine.route('/<int:id>', methods=['GET'])
def get_ventry(id):
    return_vaccine = ReturnVaccine()
    entry = ApiData.query.filter_by(id=id).first()
    if not entry:
        return make_response(f'ERROR: The requested entry was not found!', 404)
    return {'entry':return_vaccine.dump(entry)}

"""Get API Data entries based on filters"""


@vaccine.route('/', methods=['GET'])
def get_vdata():
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
def create_ventry():
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
def update_ventry(id):
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
def delete_ventry(id):
    return_vaccine = ReturnVaccine()

    entry = ApiData.query.get(id)
    if not entry:
        return make_response('ERROR: The requested entry was not found!', 404)
      
    """Delete entry from database"""      
    db.session.delete(entry)
    db.session.commit()

    return {'deleted_entry':return_vaccine.dump(entry)}

