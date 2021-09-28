from flask import Blueprint
import requests
import json


location_blueprint = Blueprint('location', __name__)

@location_blueprint.route('/')
def index():
  pass

# chave e4e5c592-d094-489f-9093-48e6c3db78a5

def api_request(origin, destination):  
  payload={}
  headers = {}

  response = requests.request(
      "GET", 
      make_url(origin, destination), 
      headers=headers, 
      data=payload
  )
  json_parsed = json.loads(response.text)
  return json_parsed['rows'][0]['elements'][0]['distance']['value']


  