import joblib

class ModelService:
    def __init__(self, model_path):
        self._model = joblib.load(model_path)

    def predict(self, features):
        return self._model.predict(features)

    def predict_proba(self, features):
        return self._model.predict_proba(features)

    def get_classes(self):
        return self._model.classes_