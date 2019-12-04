from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate = Migrate(app, db)
mail= Mail(app)

from app import routes
