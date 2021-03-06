from flask import Blueprint 
from flask import request
from flask import json
from flask.json import jsonify
from app.models import dbscan
from app.models.device_model import DeviceModel
from app.models.dbscan import ModelDBSCAN

bp = Blueprint("main", __name__, url_prefix="/ml")
device_model = DeviceModel()
dbscan = ModelDBSCAN()

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

@bp.get("/dbscan/rules")
def list_clusters():
    return jsonify({})

@bp.post("/dbscan/predict")
def cluster():
    body = request.get_json()
    if len(body["keyups"]) != 6 and len(body["keydowns"]) != 6:
        return jsonify({
            "status": 400,
            "msg": "keyups and keydowns must have 6 length",
        }), 400
    return jsonify({
        "id": dbscan.predict(request.get_json())
    }), 200


