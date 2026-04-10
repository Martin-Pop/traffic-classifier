import joblib

class ModelService:
    """
    Service that represents my model
    """

    def __init__(self, model_path):
        """
        Model must be a joblib file.
        :param model_path: path to model file
        """

        self._model = joblib.load(model_path)

    def predict(self, features):
        return self._model.predict(features)

    def predict_proba(self, features):
        return self._model.predict_proba(features)

    def get_classes(self):
        return self._model.classes_