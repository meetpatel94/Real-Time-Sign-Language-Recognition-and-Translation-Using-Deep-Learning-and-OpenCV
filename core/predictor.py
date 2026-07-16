import os
import cv2
import pickle
import numpy as np
from tensorflow.keras.models import load_model

# ==========================================
# Paths
# ==========================================

MODEL_PATH = os.path.join("models", "gesture_model.h5")
LABEL_PATH = os.path.join("models", "label_encoder.pkl")

# ==========================================
# Load Model (Only Once)
# ==========================================

model = load_model(MODEL_PATH)

print("=" * 50)
print("Model Input Shape:", model.input_shape)
print("=" * 50)

with open(LABEL_PATH, "rb") as f:
    label_encoder = pickle.load(f)
    
    print(type(label_encoder))
    print(label_encoder)

# ==========================================
# Prediction Function
# ==========================================

def predict_gesture(hand_image):
    """
    Predict hand gesture from cropped hand image.

    Returns:
        gesture (str)
        confidence (float)
    """

    try:

        if hand_image is None:
            return "Waiting", 0.0

        if hand_image.size == 0:
            return "Waiting", 0.0

        # ======================================
        # Resize (Model expects 64x64x3)
        # ======================================

        hand = cv2.resize(hand_image, (64, 64))

        # Normalize
        hand = hand.astype(np.float32) / 255.0

        # Add Batch Dimension
        hand = np.expand_dims(hand, axis=0)

        print("Before Predict:", hand.shape)

        # Prediction
        prediction = model.predict(hand, verbose=0)

        print("After Predict")

        prediction = prediction[0]

        class_index = np.argmax(prediction)

        confidence = float(prediction[class_index]) * 100

        gesture = label_encoder[class_index]
        
        print("Prediction Successful")

        return gesture, round(confidence, 2)

    except Exception as e:

        print("Prediction Error:", e)

        return "Error", 0.0