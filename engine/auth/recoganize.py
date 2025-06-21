import cv2
import face_recognition
import pickle
import numpy as np

ENCODINGS_PATH = 'engine/auth/trainer/face_encodings.pkl'

def authenticate_face():
    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)

    video = cv2.VideoCapture(0)
    match_count = 0
    MATCH_THRESHOLD = 3

    print("🔒 Face Unlock Active...")

    while True:
        ret, frame = video.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for (box, encoding) in zip(boxes, encodings):
            matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.45)
            name = "Unknown"

            face_distances = face_recognition.face_distance(data["encodings"], encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = data["names"][best_match_index]
                match_count += 1

                if match_count >= MATCH_THRESHOLD:
                    print(f"✅ Access granted to {name}")
                    video.release()
                    cv2.destroyAllWindows()
                    return True
            else:
                match_count = 0

            (top, right, bottom, left) = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0) if name != "Unknown" else (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Face Unlock", frame)
        if cv2.waitKey(1) == 27:
            break

    video.release()
    cv2.destroyAllWindows()
    print("❌ Access Denied.")
    return False

if __name__ == '__main__':
    authenticate_face()
