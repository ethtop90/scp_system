from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from backend.routes import bp


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    load_dotenv()
    CONFIG = {

    }

    CONFIG |= {} if test_config is None else test_config

    app.config.from_mapping(**CONFIG)

    app.register_blueprint(bp, url_prefix="/api")

    return app
