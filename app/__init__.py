from flask import Flask
from app.extensions import db
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    db.init_app(app)

    return app
