from typing import Optional
from app import ma
from app.models import ApiData, ScrapeData, User
from marshmallow import ValidationError, validates_schema, fields, Schema
from marshmallow.fields import Date, Email

class USState(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        us_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]

        if str(value) not in us_states:
            raise ValidationError('Location must be a valid US state (abbreviated)!')
        return str(value)
    
class Manufacturer(fields. Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        manufacturers = ['pfizer', 'Pfizer', 'janssen', 'Janssen', 'moderna', "Moderna"]

        if str(value) not in manufacturers:
            raise ValidationError('Manufacturer must be an approved manufacturer (Pfizer, Moderna or Janssen)!')
        return str(value).upper()

class Groups(fields. Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        groups = ['day', 'Day', 'Week', 'week', 'Month', 'month', 'Year', 'year']

        if str(value) not in groups:
            raise ValidationError('Aggregation must be by day, week, month or year!')
        return str(value).lower()

        
class ReturnVaccine(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiData

class AppError(Exception):
    pass

class CreateVaccine(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiData
        exclude = ("id",)

    date = fields.Date(required=True)
    location = USState(required=True)

    cols = ApiData.__table__.columns.keys()[3:]

    @validates_schema
    def validate_subset_cols(self, data, **kwargs):
        if not any(data.get(col) for col in self.cols):
            raise ValidationError('At least one statistic must be provided!')
        
class ReturnScrape(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScrapeData

class CreateScrape(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScrapeData
        exclude = ("id",)
    date = fields.Date(required=True)
    manufacturer = Manufacturer(required=True)
    location = USState(required=True)
    first_dose = fields.Integer(required=True)
    second_dose = fields.Integer(required=False)

class LoginUser(ma.SQLAlchemySchema):
    class Meta: 
        model = User
    email = fields.Email(required=True)
    password = ma.auto_field()

class CreateUser(LoginUser):
    pass

class ReturnUser(ma.SQLAlchemySchema):
    class Meta:
        model = User
    email = ma.auto_field()
    created_at = ma.auto_field()

class ReturnWeekAvg(ma.SQLAlchemySchema):

    date = fields.Date()
    avgdistjan = fields.Integer()
    avgdistmod = fields.Integer()
    avgdistpfi = fields.Integer()
    avgcomjan5 = fields.Integer()
    avgcommod5 = fields.Integer()
    avgcompfi5 = fields.Integer()
    avgcomjan12 = fields.Integer()
    avgcommod12 = fields.Integer()
    avgcompfi12 = fields.Integer()
    avgcomjan18 = fields.Integer()
    avgcommod18 = fields.Integer()
    avgcompfi18 = fields.Integer()
    avgcomjan65 = fields.Integer()
    avgcommod65 = fields.Integer()
    avgcompfi65 = fields.Integer()
    avgsecjan = fields.Integer()
    avgsecmod = fields.Integer()
    avgsecpfi = fields.Integer()

class QueryArgsSchema(Schema):
    location = fields.String()
    manufacturer = Manufacturer()
    date = fields.Date()

class AggQueryArgsSchema(Schema):
    aggregation = Groups()

        

            

