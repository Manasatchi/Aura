import os
import cv2
import face_recognition
import pickle

# Paths
ENCODINGS_PATH = 'engine/auth/trainer/face_encodings.pkl'
SAMPLES_PATH = 'engine/auth/samples'

def encode_faces():
    known_encodings = []
    known_names = []

    if not os.path.exists(SAMPLES_PATH):
        print(f"❌ Sample path '{SAMPLES_PATH}' does not exist.")
        return

    # Loop through each image in the samples directory
    for file in os.listdir(SAMPLES_PATH):
        if file.lower().endswith(".jpg"):
            path = os.path.join(SAMPLES_PATH, file)

            print(f"🔍 Processing {file}...")
            image = face_recognition.load_image_file(path)
            face_locations = face_recognition.face_locations(image)
            encodings = face_recognition.face_encodings(image, face_locations)

            if encodings:
                encoding = encodings[0]

                # Extract user ID from filename format: face.{id}.{count}.jpg
                try:
                    user_id = int(file.split('.')[1])
                    known_encodings.append(encoding)
                    known_names.append(f"User{user_id}")
                except:
                    print(f"⚠️ Could not extract user ID from filename: {file}")
            else:
                print(f"⚠️ No face found in {file}. Skipping.")

    # Save encodings and names into a .pkl file
    if known_encodings:
        os.makedirs(os.path.dirname(ENCODINGS_PATH), exist_ok=True)
        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump({"encodings": known_encodings, "names": known_names}, f)
        print(f"\n✅ Encoded {len(known_encodings)} face(s) saved to '{ENCODINGS_PATH}'")
    else:
        print("❌ No encodings were created. Check image quality or file format.")

if __name__ == '__main__':
    encode_faces()
