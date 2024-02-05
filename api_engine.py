import requests
import json
from app.utils import api_to_database

api_url = 'https://data.cdc.gov/resource/unsk-b7fc.json'

response = requests.get(api_url, params=({'$limit':38488}))

data = response.json()

json_string = json.dumps(data, indent=2)

api_to_database(data)