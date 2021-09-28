from ..src.blueprint.location_blueprint import *
from ..src.blueprint.mkad_coord import normalize_mkad, normalized_mkad

def test_id_address_valid():
  valid = "-22.322, 2.823" 
  # invalid because belongs to MKAD coordinates
  invalid = "55.785017,37.841576"

  assert is_address_valid(valid) == True
  assert is_address_valid(invalid) == False

def test_make_url():
  origin = "-22.322, 2.823" 
  destination = "37.841576,55.785017"

  url = make_url(origin, destination)

  origin = "origins=" + origin
  destination = "destinations=" + destination

  assert origin in url
  assert destination in url

def test_write_to_file():
  # write a line
  write_to_file("Ilha Solteira", "Selviria", "12 km")

  # check the last line
  f = open(".log", "r+")
  text = f.read()
  lines = text.split('\n')
  last_line = lines[len(lines) - 2]
  assert last_line == "Ilha Solteira -> Selviria: 12 km"

  #remove line
  d = f.readlines()
  f.seek(0)
  for line in d:
      if line != "Ilha Solteira -> Selviria: 12 km":
          f.write(line)
  f.truncate()

# just change the position of two sides of a string separated by a comma
# because in test statement longitude comes first
def test_normalize_mkad():
  string = normalize_mkad("gustavo,ennes")

  assert string == 'ennes,gustavo'


def test_api_request():

  invalid_destination = "91.2211,199.2201"
  no_streets_to_destination = "12.433961281999471,53.996944254523264" #Socotra island, no streets to
  destination = "33.13105398611435,44.261256045071434" #bagdá
  mkad_coord = normalized_mkad[10]

  print(mkad_coord)

  invalid_res = api_request(invalid_destination)
  no_street_res = api_request(no_streets_to_destination)
  valid_res = api_request(destination)
  mkad_res = api_request(mkad_coord)

  print("%s\n%s\n%s\n%s\n" % (invalid_res, no_street_res, valid_res, mkad_res))

  assert invalid_res == "invalid input or no streets to destination 91.2211,199.2201"
  assert no_street_res == "invalid input or no streets to destination 12.433961281999471,53.996944254523264"
  assert mkad_res == "MKAD destination coord: no output in .log file"
  assert valid_res == "3,547 km"

def test_index():
  invalid_arg = ''
  valid = '33.13105398611435,44.261256045071434'

  invalid_res = index(invalid_arg)
  valid_res = index(valid)

  assert valid_res == "3,547 km"
  assert invalid_res == "Empty destination"


