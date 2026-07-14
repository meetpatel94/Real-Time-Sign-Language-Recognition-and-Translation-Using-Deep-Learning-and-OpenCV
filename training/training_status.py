import json
import os

STATUS_FILE = os.path.join(
    "models",
    "training_status.json"
)


DEFAULT_STATUS = {

    "running": False,

    "progress": 0,

    "epoch": 0,

    "total_epochs": 0,

    "accuracy": 0,

    "loss": 0,

    "val_accuracy": 0,

    "val_loss": 0,

    "message": "Idle"

}


def save_status(data):

    os.makedirs("models", exist_ok=True)

    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def load_status():

    if not os.path.exists(
        STATUS_FILE
    ):

        save_status(
            DEFAULT_STATUS
        )

    with open(
        STATUS_FILE,
        "r"
    ) as f:

        return json.load(f)


def reset_status():

    save_status(
        DEFAULT_STATUS
    )

# ==========================================
# Stop Flag
# ==========================================

STOP_TRAINING = False


def stop_training():

    global STOP_TRAINING

    STOP_TRAINING = True


def reset_stop_flag():

    global STOP_TRAINING

    STOP_TRAINING = False


def should_stop():

    return STOP_TRAINING