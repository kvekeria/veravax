from flask import request, make_response
from flask.views import MethodView
import json
from marshmallow import ValidationError
from flask_smorest import Blueprint, abort
from app.models import ApiData
from app.schemas import ReturnVaccine, CreateVaccine, ReturnWeekAvg, AggQueryArgsSchema, QueryArgsSchema
from app import jwt_required, db
from sqlalchemy import func, TIMESTAMP, cast

vaccine = Blueprint('CDC API Vaccine Data', 'vaccine', url_prefix='/vdata', description="Endpoints to manipulate data fetched from the CDC's API on distribution by state and age.")

"""Get API Data entry by ID"""
@vaccine.route('/user')

class get_ventry(MethodView):
    @jwt_required
    def get(self, data):
        return_vaccine = ReturnVaccine()
        entry = ApiData.query.filter_by(email=data['email']).order_by(ApiData.date).first()
        if not entry:
            abort(404, f'ERROR: The requested entry was not found!')
        return {'entry':return_vaccine.dump(entry)}

"""Get all API Data"""
@vaccine.route('/')
class get_vdata(MethodView):
    @vaccine.arguments(QueryArgsSchema, location='query')
    def get(self, args):
        return_vaccine = ReturnVaccine()
        converted_data = []
        data = ApiData.query.filter_by(**args).order_by(ApiData.date).all()
        if not data:
            abort(404, 'ERROR: No entries found in the database!')
        for entry in data:
            converted_data.append(return_vaccine.dump(entry))
        return {'entries': converted_data}

"""Get API Data averages by week"""
@vaccine.route('/vweek')
class get_vweek(MethodView):
    @vaccine.arguments(AggQueryArgsSchema, location='query')
    def get(self, args):
        converted_data = []
        data = db.session.query(func.date_trunc(args['aggregation'], cast(ApiData.date, TIMESTAMP)).label('date'),
                                func.avg(ApiData.distributed_janssen).label('avgdistjan'),
                                func.avg(ApiData.distributed_pfizer).label('avgdistpfi'),
                                func.avg(ApiData.distributed_moderna).label('avgdistmod'),

                                func.avg(ApiData.series_complete_janssen_5plus).label('avgcomjan5'),
                                func.avg(ApiData.series_complete_moderna_5plus).label('avgcommod5'),
                                func.avg(ApiData.series_complete_pfizer_5plus).label('avgcompfi5'),

                                func.avg(ApiData.series_complete_janssen_12plus).label('avgcomjan12'),
                                func.avg(ApiData.series_complete_moderna_12plus).label('avgcommod12'),
                                func.avg(ApiData.series_complete_pfizer_12plus).label('avgcompfi12'),

                                func.avg(ApiData.series_complete_janssen_18plus).label('avgcomjan18'),
                                func.avg(ApiData.series_complete_moderna_18plus).label('avgcommod18'),
                                func.avg(ApiData.series_complete_pfizer_18plus).label('avgcompfi18'),

                                func.avg(ApiData.series_complete_janssen_65plus).label('avgcomjan65'),
                                func.avg(ApiData.series_complete_moderna_65plus).label('avgcommod65'),
                                func.avg(ApiData.series_complete_pfizer_65plus).label('avgcompfi65'),

                                func.avg(ApiData.second_booster_moderna).label('avgsecmod'),
                                func.avg(ApiData.second_booster_janssen).label('avgsecjan'),
                                func.avg(ApiData.second_booster_pfizer).label('avgsecpfi'),
                                ).group_by('date').order_by('date').all()
        if not data:
            abort(404, 'ERROR: No entries found in the database!')
        for entry in data:
            converted_data.append(ReturnWeekAvg().dump(entry))
        print(converted_data[0])
        return {'entries': converted_data}

"""Create API Data entry"""
@vaccine.route('/')

class create_ventry(MethodView):
    @jwt_required
    def post(self, data):
        try:
            return_vaccine = ReturnVaccine()

            """Serialize the data"""
            serialized_entry = CreateVaccine().load(json.loads(request.data))

            print(serialized_entry)

            """Convert data to API Data object"""
            database_entry = ApiData(**serialized_entry, user_id=data['user_id'])

            """Add entry to database"""
            db.session.add(database_entry)
            db.session.commit()

            return {'entry':return_vaccine.dump(database_entry)}
        
        except (ValidationError) as err:
            return make_response(str(err), 406)
    
"""Update API Data Entry"""    

@vaccine.route('/<int:id>')

class update_ventry(MethodView):
    @jwt_required
    def put(self, data):
        try:
            return_vaccine = ReturnVaccine()

            """Serialize the data"""
            serialized_entry = CreateVaccine().load(json.loads(request.data))
            
            """Convert data to API Data object"""
            database_entry = ApiData(**serialized_entry)

            entry = ApiData.query.get(id)
            if not entry:
                abort(404,'ERROR: The requested entry was not found!')

            if entry.user_id != int(data['user_id']):
                return make_response("ERROR: Cannot update another user's entry!", 403)
            
            """Update entry and add to database"""      
            entry = database_entry
            db.session.commit()

            return {'updated_entry':return_vaccine.dump(entry)}
        
        except ValidationError as err:
            return make_response(str(err), 406)

"""Delete API Data Entry"""

@vaccine.route('/<int:id>')
@jwt_required
class delete_ventry(MethodView):
    def delete(self,data,id):
        return_vaccine = ReturnVaccine()

        entry = ApiData.query.get(id)
        if not entry:
            abort(404,'ERROR: The requested entry was not found!')
        
        if entry.user_id != int(data['user_id']):
                return make_response("ERROR: Cannot delete another user's entry!", 403)
        
        """Delete entry from database"""      
        db.session.delete(entry)
        db.session.commit()

        return {'deleted_entry':return_vaccine.dump(entry)}

