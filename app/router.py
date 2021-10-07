from flask import Blueprint 
from flask import request
from flask.json import jsonify

from app.models.device_model import DeviceModel

bp = Blueprint("main", __name__, url_prefix="/ml")

@bp.get("/hello")
def hello():
    return "hello"
    
@bp.get("/device/predict")
def predict():
    # @return (deviceId & conficidence) | null
    prediction = DeviceModel().predict(request.get_json())
    return jsonify(prediction)

