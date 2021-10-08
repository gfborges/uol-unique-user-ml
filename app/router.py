from flask import Blueprint 
from flask import request
from flask.json import jsonify
from app.models.device_model import DeviceModel

from app.models.device_model import DeviceModel

bp = Blueprint("main", __name__, url_prefix="/ml")
device_model = DeviceModel()

@bp.get("/hello")
def hello():
    return "hello"
    
@bp.get("/device/predict")
def predict():
    # @return (deviceId & conficidence) | null
    prediction = DeviceModel().predict(request.get_json())
    print(prediction)
    return jsonify(prediction)

