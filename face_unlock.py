#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 13:01:01 2020

@author: chandan
"""
import numpy as np
import cv2
import face_recognition
from face_records import get_recorded_data
from sys import exit
save_path = "/etc/facelock/face_records/"

known_face_encodings,known_face_names =  get_recorded_data(save_path)
if  len(known_face_encodings)==0:
    print("facelock: No saved records")
    exit(2)



video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
passed = False
while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,model="small")

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                print(f"facelock: Authenticated by {name}")
                passed=True
                break

            face_names.append(name)

    process_this_frame = not process_this_frame


    if(passed):
        break
            
    
    
       
video_capture.release()
cv2.destroyAllWindows()



