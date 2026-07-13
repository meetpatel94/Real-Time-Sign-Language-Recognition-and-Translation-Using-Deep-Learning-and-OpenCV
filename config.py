import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "gesture_ai_project"

    MODEL_PATH = os.path.join(BASE_DIR, "model", "gesture_model.keras")

    DATASET_PATH = os.path.join(BASE_DIR, "dataset")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    DATABASE = os.path.join(BASE_DIR, "database", "recognition.db")
    
app = Flask(__name__)
app.config.from_object("config.Config")