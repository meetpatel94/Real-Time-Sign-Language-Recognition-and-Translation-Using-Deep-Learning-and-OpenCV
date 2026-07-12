from flask import Flask, render_template

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


if __name__ == "__main__":
    app.run(debug=True)