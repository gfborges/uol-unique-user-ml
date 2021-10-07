from flask import Flask

from app.models import SingletonModel

app = Flask(__name__)

def create_app():
    from dotenv import load_dotenv
    load_dotenv()
    from app.router import bp
    app.register_blueprint(bp)
    SingletonModel.load_models()
    return app
