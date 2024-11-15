import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time


bluetooth_port = '/dev/tty.HC-05'
baud_rate = 9600


mp_drawing = mp.solutions.drawing_utils




model_path = 'hand_landmarker.task'

base_options = python.BaseOptions(model_asset_path=model_path)

class GestureSender:
    def __init__(self, port: str, baud_rate: int):
        self.ser = serial.Serial(port, baud_rate)

    def send_gesture(self, gesture: str):
        try:
            command = f'{gesture}\n'
            self.ser.write(command.encode())
            print(f"Sent: {command.strip()}")
        except serial.SerialException as e:
            print(f"Error: {e}")

    def close(self):
        self.ser.close()
        print("Serial connection closed.")

options =vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

def detect_gesture(landmarks, handedness):
    """
    Detects gestures based on hand landmarks and handedness.

    Args:
        landmarks: List of hand landmarks.
        handedness: 'Left' or 'Right' indicating the detected hand.

    Returns:
        str: Detected gesture ('Forward', 'Stop', 'Left', 'Right', 'Backward', or 'Unknown').
    """
    # Define indices for palm landmarks
    PALM_LANDMARKS = [0, 1, 5, 9, 13, 17]

    # Calculate palm center
    palm_x = sum(landmarks[i].x for i in PALM_LANDMARKS) / len(PALM_LANDMARKS)
    palm_y = sum(landmarks[i].y for i in PALM_LANDMARKS) / len(PALM_LANDMARKS)

    # Define indices for fingertips and knuckles
    THUMB_TIP, THUMB_IP = 4, 3
    FINGER_TIPS = [8, 12, 16, 20]
    FINGER_PIPS = [6, 10, 14, 18]

    # Detect folded fingers
    fingers_folded = all(landmarks[tip].y > landmarks[pip].y for tip, pip in zip(FINGER_TIPS, FINGER_PIPS))
    thumb_folded = landmarks[THUMB_TIP].y > landmarks[THUMB_IP].y

    # Detect gestures
    if all(landmarks[tip].y < palm_y for tip in FINGER_TIPS):
        return "FORWARD"
    elif all(landmarks[tip].y > palm_y for tip in FINGER_TIPS):
        return "BACKWARD"
    elif fingers_folded and thumb_folded:
        return "BACKWARD"
    elif landmarks[8].y < palm_y and landmarks[12].y < palm_y and all(landmarks[i].y > palm_y for i in [16, 20]):
        return "RIGHT" if handedness == 'RIGHT' else "LEFT"
    elif landmarks[8].y < palm_y and landmarks[12].y < palm_y and landmarks[16].y < palm_y and landmarks[20].y > palm_y:
        return "LEFT" if handedness == 'RIGHT' else "RIGHT"
    else:
        return "UNKNOWN"


def process_webcam_input():
    gesture_sender = GestureSender(bluetooth_port, baud_rate)

    last_gesture = None

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            detection_result = detector.detect(mp_image)
            # detection_result.hand_landmarks[0][0].

            gesture = "UNKNOWN"

            for hand in detection_result.hand_landmarks:
                # draw_landmarks(frame, hand, HAND_CONNECTIONS)
                # draw_landmarks_on_ima
                # mp_drawing.draw_landmarks(
                #     frame,
                #     detection_result,
                #     HAND_CONNECTIONS,
                #     get_default_hand_landmarks_style(),
                #     get_default_hand_connections_style()
                # )

                gesture = detect_gesture(hand, detection_result.handedness[0][0].category_name)

                cv2.putText(frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

                if gesture != "UNKNOWN" and gesture != last_gesture:
                    gesture_sender.send_gesture(gesture)
                    last_gesture = gesture

            cv2.imshow('Gesture Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        gesture_sender.close()
        cv2.destroyAllWindows()
