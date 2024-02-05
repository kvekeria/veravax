from app import db
from sqlalchemy import Column, Integer, Double, TIMESTAMP, text, String, ForeignKey, Boolean, CheckConstraint, UniqueConstraint, Date
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship

class ApiData(db.Model):

    __tablename__ = 'api_data'

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(TIMESTAMP, server_default=('now()'), nullable=False)
    series_complete_janssen_5plus = Column(Integer)
    series_complete_moderna_5plus = Column(Integer)
    series_complete_pfizer_5plus = Column(Integer)
    series_complete_janssen_12plus = Column(Integer)
    series_complete_moderna_12plus = Column(Integer)
    series_complete_pfizer_12plus = Column(Integer)
    series_complete_janssen_18plus = Column(Integer)
    series_complete_moderna_18plus = Column(Integer)
    series_complete_pfizer_18plus = Column(Integer)
    series_complete_janssen_65plus = Column(Integer)
    series_complete_moderna_65plus = Column(Integer)
    series_complete_pfizer_65plus = Column(Integer)
    additional_doses_moderna = Column(Integer)
    additional_doses_pfizer = Column(Integer)
    additional_doses_janssen = Column(Integer)
    second_booster_moderna = Column(Integer)
    second_booster_pfizer = Column(Integer)
    second_booster_janssen = Column(Integer)
    distributed_janssen = Column(Integer)
    distributed_moderna = Column(Integer)
    distributed_pfizer = Column(Integer)
    user = relationship('User', back_populates='api_data')


cols = ApiData.__table__.columns.keys()[3:]
check_constraint = CheckConstraint(' OR '.join(f'{col} IS NOT NULL' for col in cols), name='at_least_one')
unique_constraint = UniqueConstraint('location', 'date', name='date_location_uc')
ApiData.__table__.append_constraint(unique_constraint)
ApiData.__table__.append_constraint(check_constraint)

class ScrapeData(db.Model):

    __tablename__ = 'scrape_data'

    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    first_dose = Column(Integer, nullable=False)
    second_dose = Column(Integer)
    manufacturer = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=('now()'), nullable=False)
    user = relationship('User', back_populates='scrape_data')

scrape_constraint = UniqueConstraint('location', 'date', 'manufacturer', name='date_location_sc')
ScrapeData.__table__.append_constraint(scrape_constraint)

class User(db.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # is_active = Column(Boolean, default=True, server_default=True)
    # public_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=('now()'), nullable=False)
    api_data = relationship('ApiData', back_populates='user', cascade='all, delete-orphan')
    scrape_data = relationship('ScrapeData', back_populates='user', cascade='all, delete-orphan')



        