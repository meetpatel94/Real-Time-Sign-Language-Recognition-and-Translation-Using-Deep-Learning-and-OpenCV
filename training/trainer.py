import os
import json
import pickle

from tensorflow.keras.callbacks import (
    Callback,
    ModelCheckpoint,
    EarlyStopping,
)

from training.training_status import (
    save_status,
    reset_status,
    stop_training,
    should_stop,
    reset_stop_flag,
)

from training.dataset_loader import load_dataset
from training.model import build_cnn_model

# ==========================================
# Paths
# ==========================================

DATASET_PATH = "dataset"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "gesture_model.h5"
)

LABEL_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

HISTORY_PATH = os.path.join(
    MODEL_DIR,
    "training_history.json"
)

# ==========================================
# Progress Callback
# ==========================================

class ProgressCallback(Callback):

    def __init__(self, total_epochs):

        super().__init__()

        self.total_epochs = total_epochs

    def on_epoch_end(self, epoch, logs=None):

        if logs is None:
            logs = {}

        progress = int(
            ((epoch + 1) / self.total_epochs) * 100
        )

        save_status({

            "running": True,

            "progress": progress,

            "epoch": epoch + 1,

            "total_epochs": self.total_epochs,

            "accuracy": float(
                logs.get("accuracy", 0)
            ),

            "loss": float(
                logs.get("loss", 0)
            ),

            "val_accuracy": float(
                logs.get("val_accuracy", 0)
            ),

            "val_loss": float(
                logs.get("val_loss", 0)
            ),

            "message":
                f"Epoch {epoch + 1} Completed"
                
        })
        
        if should_stop():

            self.model.stop_training = True

            save_status({

            "running": False,

            "progress": progress,

            "epoch": epoch + 1,

            "total_epochs": self.total_epochs,

            "accuracy": float(logs.get("accuracy", 0)),

            "loss": float(logs.get("loss", 0)),

            "val_accuracy": float(logs.get("val_accuracy", 0)),

            "val_loss": float(logs.get("val_loss", 0)),

            "message": "Training Stopped"

        })

        

# ==========================================
# Train Model
# ==========================================

def train_model(

    epochs=30,

    batch_size=32,

):

    os.makedirs(

        MODEL_DIR,

        exist_ok=True,

    )

    # Reset Previous Status

    reset_status()
    reset_stop_flag()

    save_status({

        "running": True,

        "progress": 0,

        "epoch": 0,

        "total_epochs": epochs,

        "accuracy": 0,

        "loss": 0,

        "val_accuracy": 0,

        "val_loss": 0,

        "message": "Loading Dataset..."

    })

    # Load Dataset

    X_train, X_test, y_train, y_test, class_names = load_dataset(

        DATASET_PATH

    )

    save_status({

        "running": True,

        "progress": 0,

        "epoch": 0,

        "total_epochs": epochs,

        "accuracy": 0,

        "loss": 0,

        "val_accuracy": 0,

        "val_loss": 0,

        "message": "Building CNN Model..."

    })

    model = build_cnn_model(

        len(class_names)

    )

    callbacks = [

        ModelCheckpoint(

            MODEL_PATH,

            monitor="val_accuracy",

            save_best_only=True,

            verbose=1,

        ),

        EarlyStopping(

            monitor="val_loss",

            patience=5,

            restore_best_weights=True,

        ),

        ProgressCallback(

            epochs

        )

    ]
    # ==========================================
    # Start Training
    # ==========================================

    history = model.fit(

        X_train,

        y_train,

        validation_data=(

            X_test,

            y_test,

        ),

        epochs=epochs,

        batch_size=batch_size,

        callbacks=callbacks,

        verbose=1,

    )

    # ==========================================
    # Save Label Encoder
    # ==========================================

    with open(

        LABEL_PATH,

        "wb",

    ) as f:

        pickle.dump(

            class_names,

            f,

        )

    # ==========================================
    # Save Training History
    # ==========================================

    with open(

        HISTORY_PATH,

        "w",

    ) as f:

        json.dump(

            history.history,

            f,

            indent=4,

        )

    # ==========================================
    # Evaluate Model
    # ==========================================

    loss, accuracy = model.evaluate(

        X_test,

        y_test,

        verbose=0,

    )

    # ==========================================
    # Final Status
    # ==========================================

    if should_stop():

        save_status({

            "running": False,

            "progress": progress,

            "epoch": history.epoch[-1] + 1,

            "total_epochs": epochs,

            "accuracy": float(accuracy),

            "loss": float(loss),

            "val_accuracy": float(

                history.history["val_accuracy"][-1]

            ),

            "val_loss": float(

                history.history["val_loss"][-1]

            ),

            "message": "Training Stopped"

        })

    else:

        save_status({

            "running": False,

            "progress": 100,

            "epoch": epochs,

            "total_epochs": epochs,

            "accuracy": float(accuracy),

            "loss": float(loss),

            "val_accuracy": float(

                history.history["val_accuracy"][-1]

            ),

            "val_loss": float(

                history.history["val_loss"][-1]

            ),

            "message": "Training Completed"

        })

    # ==========================================
    # Return Result
    # ==========================================

    return {

        "accuracy": float(accuracy),

        "loss": float(loss),

        "classes": class_names,

        "history": history.history,

    }