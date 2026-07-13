import os
import cv2
import threading
import time

from datetime import datetime
from core.camera import get_latest_frame

is_collecting = False
gesture_name = ""
target_images = 0
current_count = 0

def start_collection(gesture, total):

    global is_collecting
    global gesture_name
    global target_images
    global current_count

    gesture_name = gesture.strip().upper()
    target_images = int(total)
    current_count = 0
    is_collecting = True

    folder = os.path.join("dataset", gesture_name)

    os.makedirs(folder, exist_ok=True)

    return True


def stop_collection():

    global is_collecting

    is_collecting = False


def collection_status():

    return {

        "collecting": is_collecting,
        "gesture": gesture_name,
        "current": current_count,
        "total": target_images

    }


def save_image():

    global current_count
    global is_collecting

    if not is_collecting:
        return

    frame = get_latest_frame()
    if frame is None:
        return

    if current_count >= target_images:

        is_collecting = False
        return

    folder = os.path.join("dataset", gesture_name)

    filename = f"{current_count+1:04}.jpg"

    filepath = os.path.join(folder, filename)

    cv2.imwrite(filepath, frame)

    current_count += 1
    
def auto_collect():

    global is_collecting

    while True:

        if is_collecting:

            save_image()

            if current_count >= target_images:

                is_collecting = False

        time.sleep(0.20)


collector_thread = threading.Thread(
    target=auto_collect,
    daemon=True
)

collector_thread.start()


def dataset_summary():

    dataset_path = "dataset"

    total_classes = 0
    total_images = 0

    if not os.path.exists(dataset_path):

        return {
            "classes": 0,
            "images": 0,
            "training": 0,
            "testing": 0
        }

    for folder in os.listdir(dataset_path):

        folder_path = os.path.join(dataset_path, folder)

        if os.path.isdir(folder_path):

            total_classes += 1

            images = len([
                f for f in os.listdir(folder_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ])

            total_images += images

    training = int(total_images * 0.80)
    testing = total_images - training

    return {

        "classes": total_classes,

        "images": total_images,

        "training": training,

        "testing": testing

    }


def dataset_table():

    dataset_path = "dataset"

    rows = []

    if not os.path.exists(dataset_path):

        return rows

    for folder in sorted(os.listdir(dataset_path)):

        folder_path = os.path.join(dataset_path, folder)

        if not os.path.isdir(folder_path):
            continue

        images = len([
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])

        rows.append({

            "gesture": folder,

            "images": images,

            "training": int(images * 0.80),

            "testing": images - int(images * 0.80),

            "status": "Ready" if images > 0 else "Empty"

        })

    return rows