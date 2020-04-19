from flask import Flask, request
from flask_sslify import SSLify
from flask_cors import CORS

from app.router import routers, exempt
from app.models import config_init

app = Flask(__name__)
sslify = SSLify(app)
CORS(app)

config_init('configure.ini')

routers(app)
exempt(app)
