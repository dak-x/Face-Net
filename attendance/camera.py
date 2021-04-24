import cv2

cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)
import os
import face_recognition
import cv2
import numpy as np
# new_face_encodings=[]
# new_face_names=[]
# for filename in os.listdir('attendance/datasets'):
#     if(filename!='.ipynb_checkpoints' and filename!='.DS_Store'):
#             test = face_recognition.load_image_file(os.path.join('attendance/datasets',filename))
#             test_encoding = face_recognition.face_encodings(test)[0]
#             new_face_encodings.append(test_encoding)
#             face_name = filename.split('.')[0][:-1]
#             new_face_names.append(face_name)
# known_face_encodings = new_face_encodings
# known_face_names = new_face_names
video_capture = cv2.VideoCapture(0)  # 0 for web camera live stream
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'

def authenticate(userID):
    test_face_encodings = []
    try:
        test = face_recognition.load_image_file(os.path.join('attendance/datasets',userID+".png"))
    except:
        test = face_recognition.load_image_file(os.path.join('attendance/datasets',userID+".jpg"))
    try:
        test_encoding = face_recognition.face_encodings(test)[0]
        test_face_encodings.append(test_encoding)
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]

        face_distances = face_recognition.face_distance(test_face_encodings, face_encoding)
        if (min(face_distances) > 0.4):
            print(min(face_distances))
            return False
        else:
            print(min(face_distances))
            return True
    except Exception as e:
        print(e)
        return authenticate(userID)


def camera_stream():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        return cv2.imencode('.jpg', frame)[1].tobytes()


