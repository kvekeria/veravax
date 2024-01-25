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
                db.session.add(new_entry)
                db.session.commit()

def scrape_to_database(entries, manufacturer):
    entries = [x.text for x in entries]
    entries = [entries[x:x+3] for x in range(0, len(entries), 3)]

    for entry in entries:
        new_entry = ScrapeData(location=entry[0], date=entry[1], 
                               number=convert_to_int(entry[2]), manufacturer=manufacturer)

        with app.app_context():
            with db.session.begin():
                exists = ScrapeData.query.filter_by(location=new_entry.location, 
                                                    date=new_entry.date, number=new_entry.number, 
                                                    manufacturer=new_entry.manufacturer).first()

                if not exists:
                    db.session.add(new_entry)
                    db.session.commit()