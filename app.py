from flask import Flask, render_template, Response, jsonify, request

from core.camera import (
    generate_frames,
    capture_frame,
    start_camera,
    stop_camera,
    clear_dataset,
    is_camera_running,
    get_camera_status,
    start_dataset_collection,
    stop_dataset_collection,
    get_dataset_status
)

from core.dataset import (
    dataset_summary,
    dataset_table
)

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
        page_subtitle="Train AI Model"
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
        page_subtitle="Analytics Dashboard"
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
        page_subtitle="Gesture Translation"
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
        page_subtitle="Application Settings"
    )

# ==========================================
# About
# ==========================================

@app.route("/about")
def about():
    return render_template(
        "about.html",
        active_page="about",
        page_title="About Project",
        page_subtitle="Project Information"
    )

# ==========================================
# Camera APIs
# ==========================================

@app.route("/start_camera")
def start_camera_route():

    if start_camera():

        return jsonify({
            "status": "started"
        })

    return jsonify({
        "status": "failed"
    })

@app.route("/stop_camera")
def stop_camera_route():

    stop_camera()

    return jsonify({
        "status": "stopped"
    })

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
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
    
# ==========================================
# Live Status API
# ==========================================

@app.route("/status")
def status():

    return jsonify(
        get_camera_status()
    )


# ==========================================
# Dataset APIs
# ==========================================

@app.route("/start_collection", methods=["POST"])
def start_collection_route():

    data = request.get_json()

    gesture = data.get("gesture", "").strip()
    total = int(data.get("total", 500))

    if gesture == "":

        return jsonify({

            "status": "error",

            "message": "Gesture Name Required"

        })

    if not is_camera_running():

        start_camera()

    start_dataset_collection(
        gesture,
        total
    )

    return jsonify({

        "status": "success"

    })


@app.route("/stop_collection")
def stop_collection_route():

    stop_dataset_collection()

    return jsonify({

        "status": "stopped"

    })

# ==========================================
# Clear Dataset Collection
# ==========================================

@app.route("/clear_collection")
def clear_collection_route():

    clear_dataset()

    return jsonify({

        "status": "cleared"

    })

@app.route("/collection_status")
def collection_status_route():

    return jsonify(
        get_dataset_status()
    )


# ==========================================
# Dataset Information
# ==========================================

@app.route("/dataset_info")
def dataset_info():

    return jsonify({

        "summary": dataset_summary(),

        "table": dataset_table()

    })


# ==========================================
# Future APIs
# ==========================================

@app.route("/prediction")
def prediction():

    return jsonify({

        "gesture": "Waiting",

        "confidence": 0

    })


@app.route("/translation_api")
def translation_api():

    return jsonify({

        "text": ""

    })


@app.route("/history_api")
def history_api():

    return jsonify([])


@app.route("/analytics_api")
def analytics_api():

    return jsonify({

        "accuracy": 0,

        "fps": 0,

        "predictions": 0

    })


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )