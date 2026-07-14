from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout,
    BatchNormalization,
)
from tensorflow.keras.optimizers import Adam


IMAGE_SIZE = 64


def build_cnn_model(num_classes):
    """
    Build CNN model for hand gesture recognition.
    """

    model = Sequential([

        Conv2D(
            32,
            (3, 3),
            activation="relu",
            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
        ),
        BatchNormalization(),
        MaxPooling2D((2, 2)),


        Conv2D(
            64,
            (3, 3),
            activation="relu",
        ),
        BatchNormalization(),
        MaxPooling2D((2, 2)),


        Conv2D(
            128,
            (3, 3),
            activation="relu",
        ),
        BatchNormalization(),
        MaxPooling2D((2, 2)),


        Flatten(),

        Dense(
            256,
            activation="relu",
        ),

        Dropout(0.5),

        Dense(
            num_classes,
            activation="softmax",
        ),
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model