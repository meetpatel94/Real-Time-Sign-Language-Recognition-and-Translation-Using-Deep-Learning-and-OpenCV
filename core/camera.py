import cv2
import os
import mediapipe as mp
import time
from datetime import datetime

# ==========================================
# Global Variables
# ==========================================

camera = None
latest_frame = None
camera_running = False

# Live Status

hand_detected = False
camera_fps = 0

# Dataset Collection

dataset_mode = False
dataset_gesture = ""
dataset_target = 0
dataset_count = 0
last_save_time = 0

# ==========================================
# MediaPipe Initialization
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================================
# Camera Functions
# ==========================================

def start_camera():

    global camera
    global camera_running

    if camera is None:

        camera = cv2.VideoCapture(0)

        camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    camera_running = camera.isOpened()

    return camera_running


def stop_camera():

    global camera
    global camera_running

    if camera is not None:

        camera.release()

        camera = None

    camera_running = False
 
    hand_detected = False
    camera_fps = 0


def is_camera_running():

    return camera_running


def get_latest_frame():

    global latest_frame

    if latest_frame is None:
        return None

    return latest_frame.copy()

# ==========================================
# Dataset Functions
# ==========================================

def start_dataset_collection(gesture, total):

    global dataset_mode
    global dataset_gesture
    global dataset_target
    global dataset_count

    gesture = gesture.upper().strip()

    folder = os.path.join("dataset", gesture)

    os.makedirs(folder, exist_ok=True)

    existing_images = len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    dataset_mode = True
    dataset_gesture = gesture
    dataset_target = int(total)

    # Resume from existing images
    dataset_count = existing_images


def stop_dataset_collection():

    global dataset_mode

    dataset_mode = False

    stop_camera()
    
def clear_dataset():

    global dataset_mode
    global dataset_gesture
    global dataset_target
    global dataset_count
    global latest_frame

    dataset_mode = False
    dataset_gesture = ""
    dataset_target = 0
    dataset_count = 0
    latest_frame = None


def get_dataset_status():

    return{

        "running":dataset_mode,

        "gesture":dataset_gesture,

        "current":dataset_count,

        "target":dataset_target

    }
    # ==========================================
# Live Camera Stream
# ==========================================

def generate_frames():

    global camera
    global latest_frame
    global dataset_count
    global dataset_mode
    global hand_detected
    global camera_fps
    global last_save_time

    prev_time = time.time()
    while True:

        if camera is None:
            break

        success, frame = camera.read()
        current_time = time.time()

        time_diff = current_time - prev_time

        if time_diff > 0:
            camera_fps = int(1 / time_diff)
        else:
            camera_fps = 0

        prev_time = current_time

        if not success:
            break

        frame = cv2.flip(frame, 1)

        latest_frame = frame.copy()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        hand_detected = False

        if results.multi_hand_landmarks:

            hand_detected = True

            h, w, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                    mp_draw.DrawingSpec(color=(255,0,0), thickness=2)
                )

                x_list = []
                y_list = []

                for lm in hand_landmarks.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    x_list.append(x)
                    y_list.append(y)

                xmin = max(min(x_list) - 20, 0)
                ymin = max(min(y_list) - 20, 0)

                xmax = min(max(x_list) + 20, w)
                ymax = min(max(y_list) + 20, h)

                cv2.rectangle(
                    frame,
                    (xmin, ymin),
                    (xmax, ymax),
                    (255,255,0),
                    2
                )

                # =========================
                # Dataset Collection
                # =========================

                if dataset_mode:

                    if dataset_count < dataset_target:

                        hand = latest_frame[ymin:ymax, xmin:xmax]

                        if hand.size != 0:

                            hand = cv2.resize(hand, (224,224))

                            filename = os.path.join(
                            "dataset",
                            dataset_gesture,
                            f"{dataset_count + 1:04d}.jpg"
                        )

                            current_time = time.time()

                            if current_time - last_save_time > 0.30:

                                cv2.imwrite(filename, hand)

                                dataset_count += 1

                                last_save_time = current_time

                            cv2.putText(
                                frame,
                                f"Saved : {dataset_count}/{dataset_target}",
                                (20,40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0,255,0),
                                2
                            )

                    else:

                        dataset_mode = False

                        cv2.putText(
                            frame,
                            "Collection Completed",
                            (20,40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,255,0),
                            2
                        )

        if not hand_detected:

            cv2.putText(
                frame,
                "No Hand Detected",
                (20,90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
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
        # ==========================================
# Capture Single Image
# ==========================================

def capture_frame():

    global latest_frame

    if latest_frame is None:
        return None

    os.makedirs("captured_images", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    filepath = os.path.join(
        "captured_images",
        filename
    )

    cv2.imwrite(filepath, latest_frame)

    return filename


# ==========================================
# Camera Status
# ==========================================

def get_camera_status():

    return {

        "camera": camera_running,

        "dataset_mode": dataset_mode,

        "gesture": dataset_gesture,

        "current": dataset_count,

        "target": dataset_target,

        "hand": hand_detected,

        "fps": camera_fps

    }