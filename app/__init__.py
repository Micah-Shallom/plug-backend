from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    db.init_app(app)
    
    migrate = Migrate(app,db)
    

    return app

