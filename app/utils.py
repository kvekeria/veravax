from app.models import ApiData, ScrapeData
from app import app, db

def convert_to_int(number):
    return int(number.replace(',',''))

def api_to_database(data):
    cols = ApiData.__table__.columns.keys()
    for entry in data:
        new_entry = ApiData()
        for key in cols:
            if key in entry:
                setattr(new_entry, key, entry[f'{key}'])
        with app.app_context():
            with db.session.begin():
                if new_entry.date is not None or new_entry.location is not None:
                    exists = db.session.query(ApiData).filter_by(date=new_entry.date, location=new_entry.location).first()
                    if exists:
                        exists = new_entry
                        db.session.commit()
                    else:
                        db.session.add(new_entry)
                        db.session.commit()

def scrape_janssen_to_database(entries):
    entries = [x.text for x in entries]
    entries = [entries[x:x+3] for x in range(0, len(entries), 3)]

    for entry in entries:
        new_entry = ScrapeData(location=entry[0], date=entry[1], 
                               first_dose=convert_to_int(entry[2]), manufacturer='Janssen')

        with app.app_context():
            with db.session.begin():
                exists = db.session.query(ScrapeData).filter_by(location=new_entry.location, 
                                                    date=new_entry.date, first_dose=new_entry.first_dose, 
                                                    manufacturer=new_entry.manufacturer).first()

                if not exists:
                    db.session.add(new_entry)
                    db.session.commit()
                else:
                    exists = new_entry
                    db.session.commit()

def scrape_to_database(entries, manufacturer):
    entries = [x.text for x in entries]
    entries = [entries[x:x+4] for x in range(0, len(entries), 4)]

    for entry in entries:
        new_entry = ScrapeData(location=entry[0], date=entry[1], 
                               first_dose=convert_to_int(entry[2]), second_dose=convert_to_int(entry[3]), manufacturer=manufacturer)

        with app.app_context():
            with db.session.begin():
                exists = db.session.query(ScrapeData).filter_by(location=new_entry.location, 
                                                    date=new_entry.date, first_dose=new_entry.first_dose,
                                                    second_dose=new_entry.second_dose, 
                                                    manufacturer=new_entry.manufacturer).first()

                if not exists:
                    db.session.add(new_entry)
                    db.session.commit()
                else:
                    exists = new_entry
                    db.session.commit()