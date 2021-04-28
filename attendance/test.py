import cv2
import cv2

cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)
import os
import face_recognition
import cv2
import numpy as np
video_capture = cv2.VideoCapture(0) 
def authenticate(userID):
    test_face_encodings = []
    try:
        test = face_recognition.load_image_file(os.path.join('attendance/datasets',userID+".png"))
    except:
        test = face_recognition.load_image_file(os.path.join('attendance/datasets',userID+".jpg"))
    try:
        # video_capture = cv2.VideoCapture(0)
        # cv2.destroyAllWindows()
        # video_capture.release()
        
        test_encoding = face_recognition.face_encodings(test)[0]
        test_face_encodings.append(test_encoding)
        print("*****************************************************************************************")
        print(test.shape)
        ret, frame = video_capture.read()
        print("*****************************************************************************************")
        print(frame.shape)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]

        face_distances = face_recognition.face_distance(test_face_encodings, face_encoding)
        if (min(face_distances) > 0.4):
            print(min(face_distances))
            video_capture.release()
            return False
        else:
            print(min(face_distances))
            video_capture.release()
            return True

    except Exception as e:
        print(e)
        return authenticate(userID)

print(authenticate("2018"))