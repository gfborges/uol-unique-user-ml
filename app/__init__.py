from flask import Flask

app = Flask(__name__)

def create_app():
    from app.router import bp
    app.register_blueprint(bp)
    return app
