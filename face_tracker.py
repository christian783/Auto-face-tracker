import cv2
import serial
import time

# --- Setup serial communication ---
arduino = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)  # Give connection time to establish

# --- OpenCV Setup ---
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

FRAME_CENTER_TOLERANCE = 50  # pixels

while True:
    ret, frame = camera.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]  # take the first face detected
        face_center_x = x + w // 2
        frame_center_x = frame.shape[1] // 2

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]), (255, 0, 0), 2)

        diff = face_center_x - frame_center_x

        if abs(diff) < FRAME_CENTER_TOLERANCE:
            command = 'S'  # Stop
        elif diff > 0:
            command = 'R'  # Face is right → turn motor right
        else:
            command = 'L'  # Face is left → turn motor left

        arduino.write(command.encode())
    else:
        # No face detected → stop motor
        arduino.write(b'S')

    cv2.imshow("Auto Face Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
arduino.close()
