import cv2
import os
import mediapipe as mp
from datetime import datetime

camera = None
latest_frame = None

def get_latest_frame():
    global latest_frame

    if latest_frame is None:
        return None

    return latest_frame.copy()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def start_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera.isOpened()

def stop_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    global camera, latest_frame

    while True:
        if camera is None:
            break

        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        latest_frame = frame.copy()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            h, w, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                x_list = []
                y_list = []

                for lm in hand_landmarks.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    x_list.append(x)
                    y_list.append(y)

                xmin = min(x_list)
                xmax = max(x_list)
                ymin = min(y_list)
                ymax = max(y_list)

                cv2.rectangle(
                    frame,
                    (xmin - 20, ymin - 20),
                    (xmax + 20, ymax + 20),
                    (255, 255, 0),
                    2
                )

                if results.multi_handedness:
                    label = results.multi_handedness[0].classification[0].label

                    cv2.putText(
                        frame,
                        label,
                        (xmin, ymin - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

def capture_frame():
    global latest_frame

    if latest_frame is None:
        return None

    os.makedirs("captured_images", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join("captured_images", filename)

    cv2.imwrite(filepath, latest_frame)

    return filename