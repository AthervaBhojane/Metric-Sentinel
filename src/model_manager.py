import joblib
import os

MODEL_PATH = "models/anomaly_model.pkl"


def save_model(model):

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    joblib.dump(model, MODEL_PATH)


def load_model():

    if os.path.exists(MODEL_PATH):

        return joblib.load(
            MODEL_PATH
        )

    return None