from typing import Optional
from app import ma
from app.models import ApiData, ScrapeData, User
from marshmallow import ValidationError, validates_schema, fields
from marshmallow.fields import Date

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



        

            

