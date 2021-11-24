

class SingletonModel(type):
    _instances = {}

    def __call__(cls, *args: list, **kwds: dict):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]


    @classmethod
    def load_models(cls):
        from app.models.device_model import DeviceModel
        from app.models.dbscan import ModelDBSCAN
        DeviceModel()
        ModelDBSCAN()
        




