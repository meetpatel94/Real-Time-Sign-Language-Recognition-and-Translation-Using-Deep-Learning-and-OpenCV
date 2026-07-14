import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

IMAGE_SIZE = 64


def load_dataset(dataset_path):
    """
    Load gesture dataset from folders.

    dataset/
        A/
        B/
        C/

    Returns:
        X_train
        X_test
        y_train
        y_test
        class_names
    """

    images = []
    labels = []

    class_names = sorted(
        [
            folder
            for folder in os.listdir(dataset_path)
            if os.path.isdir(os.path.join(dataset_path, folder))
        ]
    )

    class_to_index = {
        name: idx
        for idx, name in enumerate(class_names)
    }

    for class_name in class_names:

        class_folder = os.path.join(dataset_path, class_name)

        for file in os.listdir(class_folder):

            path = os.path.join(class_folder, file)

            image = cv2.imread(path)

            if image is None:
                continue

            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image = image.astype("float32") / 255.0

            images.append(image)

            labels.append(class_to_index[class_name])

    X = np.array(images, dtype=np.float32)

    y = np.array(labels)

    y = to_categorical(y, num_classes=len(class_names))

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        shuffle=True,
        stratify=np.argmax(y, axis=1),
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        class_names,
    )