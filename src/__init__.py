from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from .extensions import api, db, jwt, migration, mail
from .routes import ns
from flask_cors import CORS

# import models to let the migrate tool know
from .models.models import User, StudentTeacherRelation, Subject, User_logins, Rol

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# To specify the secret work for jwt auth
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# Config for mailing
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = FLASK_MAIL_USER
app.config['MAIL_PASSWORD'] = FLASK_MAIL_PW
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# mail instance
mail.init_app(app)

# sql alchemy instance
db.init_app(app)

# Para evitar el crossOrigin CORS error
CORS(app)

# api instance
api.init_app(app)

# jwt instance
jwt.init_app(app)

# Flask Migrate instance to handle migrations
migration.init_app(app, db)

#  INSTANCIACION DE NAMESPACE (/api/servicio), SE USA EN ROUTES, PARA LAS RUTAS DE LOS SERVICIOS, MARSHALING...
api.add_namespace(ns)

# Callback para el createAccessToken, que hay que pasarle un dato JSONSerializable
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()
    
