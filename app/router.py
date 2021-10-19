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

@bp.get("/device/rules")
def list_rules():
    rules = [rule.to_json() for rule in device_model.rules]
    return jsonify(rules)

@bp.post("/device/predict")
def predict():
    # @return (deviceId & conficidence) | null
    prediction = device_model.predict(request.get_json())
    if prediction:
        return jsonify(prediction.to_json())
    return jsonify({"statusCode": 404, "msg": "No rule matched"}), 404

