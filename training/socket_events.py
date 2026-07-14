from flask_socketio import emit


def send_training_progress(
    socketio,
    epoch,
    total_epochs,
    accuracy,
    loss,
    val_accuracy,
    val_loss,
):

    print(f"Sending Progress : {epoch}/{total_epochs}")

    progress = int((epoch / total_epochs) * 100)

    socketio.emit(
        "training_progress",
        {
            "epoch": epoch,
            "total_epochs": total_epochs,
            "progress": progress,
            "accuracy": float(accuracy),
            "loss": float(loss),
            "val_accuracy": float(val_accuracy),
            "val_loss": float(val_loss),
        },
    )

    socketio.sleep(0)