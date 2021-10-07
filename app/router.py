from flask import Blueprint 
from flask import request
from flask.json import jsonify

bp = Blueprint("main", __name__, url_prefix="/ml")

@bp.get("/hello")
def hello():
    return "hello"
    
@bp.get("/device/predict")
def predict():
    request.get_json()
    return jsonify({})

