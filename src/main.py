from flask import Flask
from flask_cors import CORS
from .controllers import currencies_bp

app = Flask(__name__)

app.register_blueprint(currencies_bp, url_prefix='/api/v1')


