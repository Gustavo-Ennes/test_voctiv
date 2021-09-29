from flask import Flask
from dotenv import load_dotenv
from .location_blueprint import location_blueprint

# loading environment variable for google api key
load_dotenv()

app = Flask(__name__)
app.register_blueprint(location_blueprint)
