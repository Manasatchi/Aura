import cv2
import os
import numpy as np
from PIL import Image
from datetime import datetime
import pyttsx3

def capture_samples():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    face_id = input("Enter a numeric user ID: ")
    save_dir = 'engine/auth/samples'
    os.makedirs(save_dir, exist_ok=True)

    face_detector = cv2.CascadeClassifier('engine/auth/haarcascade_frontalface_default.xml')
    print("Taking samples. Look at the camera...")
    count = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite(f"{save_dir}/face.{face_id}.{count}.jpg", gray[y:y+h, x:x+w])
            cv2.imshow('Capturing Face', img)

        k = cv2.waitKey(100) & 0xff
        if k == 27 or count >= 300:
            break

    print("Samples taken. Exiting...")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
        capture_samples()