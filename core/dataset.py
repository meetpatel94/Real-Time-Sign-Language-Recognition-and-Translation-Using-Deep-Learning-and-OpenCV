import os
import shutil

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

# ==========================================
# Delete Gesture Folder
# ==========================================

def delete_gesture(gesture):

    folder = os.path.join("dataset", gesture.upper())

    if not os.path.exists(folder):

        return False

    shutil.rmtree(folder)

    return True

# ==========================================
# View Gesture Images
# ==========================================

def view_gesture_images(gesture):

    folder = os.path.join(
        "dataset",
        gesture.upper()
    )

    if not os.path.exists(folder):

        return []

    images = []

    for file in sorted(os.listdir(folder)):

        if file.lower().endswith((".jpg", ".jpeg", ".png")):

            images.append(file)

    return images
