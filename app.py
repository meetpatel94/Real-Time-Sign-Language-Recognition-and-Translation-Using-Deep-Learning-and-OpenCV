from flask import Flask, render_template, Response, jsonify
from flask import Flask, render_template
from flask import Flask, render_template, Response
from flask import jsonify
from flask import request, jsonify

from core.dataset import (
    start_collection,
    stop_collection,
    collection_status,
    dataset_summary,
    dataset_table
)
from core.camera import generate_frames, capture_frame, start_camera, stop_camera, camera

app = Flask(__name__)


# ==========================================
# Dashboard
# ==========================================
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        page_title="Dashboard",
        page_subtitle="Real-Time Hand Gesture Recognition"
    )


# ==========================================
# Dataset
# ==========================================
@app.route("/dataset")
def dataset():
    return render_template(
        "dataset.html",
        active_page="dataset",
        page_title="Dataset",
        page_subtitle="Manage Gesture Dataset"
    )


# ==========================================
# Model Training
# ==========================================
@app.route("/model-training")
def model_training():
    return render_template(
        "model_training.html",
        active_page="model_training",
        page_title="Model Training",
        page_subtitle="Train & Evaluate AI Model"
    )


# ==========================================
# Live Recognition
# ==========================================
@app.route("/live-recognition")
def live_recognition():
    return render_template(
        "live_recognition.html",
        active_page="live_recognition",
        page_title="Live Recognition",
        page_subtitle="Real-Time Camera Detection"
    )


# ==========================================
# History
# ==========================================
@app.route("/history")
def history():
    return render_template(
        "history.html",
        active_page="history",
        page_title="History",
        page_subtitle="Recognition History"
    )


# ==========================================
# Analytics
# ==========================================
@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        active_page="analytics",
        page_title="Analytics",
        page_subtitle="System Analytics & Reports"
    )


# ==========================================
# Translation
# ==========================================
@app.route("/translation")
def translation():
    return render_template(
        "translation.html",
        active_page="translation",
        page_title="Translation",
        page_subtitle="Sign Language Translation"
    )


# ==========================================
# Settings
# ==========================================
@app.route("/settings")
def settings():
    return render_template(
        "settings.html",
        active_page="settings",
        page_title="Settings",
        page_subtitle="Application Configuration"
    )


# ==========================================
# About Project
# ==========================================
@app.route("/about")
def about():
    return render_template(
        "about.html",
        active_page="about",
        page_title="About Project",
        page_subtitle="Project Information & Documentation"
    )
    
@app.route("/status")
def status():

    return jsonify({

        "camera": camera is not None,

        "prediction": "HAND DETECTED",

        "confidence": "100%",

        "fps": 30,

        "model": "CNN"

    })
    
@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
    
@app.route("/capture")
def capture():

    filename = capture_frame()

    if filename:

        return jsonify({
            "status": "success",
            "filename": filename
        })

    return jsonify({
        "status": "error"
    })
    
@app.route("/start_camera")
def start_camera_route():

    if start_camera():

        return {
            "status": "started"
        }

    return {
        "status": "failed"
    }
    
@app.route("/stop_camera")
def stop_camera_route():

    stop_camera()

    return {
        "status": "stopped"
    }

@app.route("/start_collection", methods=["POST"])
def start_dataset_collection():

    data = request.get_json()

    gesture = data.get("gesture")
    total = data.get("total")

    if not gesture:
        return jsonify({
            "status": "error",
            "message": "Gesture Name Required"
        })

    start_collection(gesture, total)

    return jsonify({
        "status": "success"
    })
    
@app.route("/stop_collection")
def stop_dataset_collection():

    stop_collection()

    return jsonify({
        "status": "stopped"
    })

@app.route("/collection_status")
def get_collection_status():

    return jsonify(collection_status())

@app.route("/dataset_info")
def dataset_info():

    return jsonify({

        "summary": dataset_summary(),

        "table": dataset_table()

    })

if __name__ == "__main__":
    app.run(debug=True)
    