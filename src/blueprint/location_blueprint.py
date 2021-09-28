from flask import Blueprint
import requests
import json
import os
import traceback
from .mkad_coord import normalized_mkad
from dotenv import load_dotenv

load_dotenv()


location_blueprint = Blueprint('location', __name__)

@location_blueprint.route('/<destination>/')
def index(destination):
  # if destination isn't a empty string
  if(destination):
    res = api_request(destination)
    return res
  else:
    return "Empty destination"


def is_address_valid(add):
    return not add in normalized_mkad


def make_url(origin, destination):
    # origin = urllib.parse.quote(origin)
    # destination = urllib.parse.quote(destination)
    return "https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s" % (origin, destination, os.getenv("GDM_API_KEY"))
    

def write_to_file(origin, destination, meters):
    f = open(".log", "a")
    f.write("%s -> %s: %s\n" % (origin, destination,meters))
    f.close()


# API request method, return distance in meters or an error message
# args can be a name of a city or a coord
def api_request(destination):  
  try:

    if(is_address_valid(destination)):
      # origin is mkad km 1
      origin = normalized_mkad[0]
      print("origin: %s" % origin)
      print("Destination: %s" % destination)

      # get response
      url = make_url(origin, destination)
      response = requests.request("GET", url)

      print("url: %s" % url)

      # parse it
      json_parsed = json.loads(response.text)

      # string name to put in .log file
      origin_name = json_parsed['origin_addresses'][0]
      destination_name = json_parsed['destination_addresses'][0]

      # get meters
      kilometers = json_parsed['rows'][0]['elements'][0]['distance']['text']
      # write to a .log file
      write_to_file(origin_name, destination_name, kilometers)
      return kilometers
    else:
      return "MKAD destination coord: no output in .log file"
  except:
    # returning a invalid destination or origin
    print(traceback.format_exc())
    return "invalid input or no streets to destination %s" % (destination)


# I'm using distance matrix, from google apis
# The Yandex api is kind of confusing and they don't give me a working api key
# unless I get a plan, 1000 request a day for $2000/month
def make_url(origin, destination):
    return "https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s" % (origin, destination, os.getenv("GDM_API_KEY"))




  