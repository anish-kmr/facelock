#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from face_detect import get_face_encodings
from face_records import save_new_encoding,get_recorded_data
from numpy import argmin
import cv2
from os.path import isdir
import face_recognition as fr


def validate_file(file):
    if isdir(file):
        return f"facelock: {file} is a Directory. Image File Required"
    else:
        extension = file.split(".")[1]
        if(extension not in ["jpg","png","jpeg"]):
            return f' facelock: "jpg","png","jpeg" supprted. {extension} given'
        else:
            return "ok"




def add_face_via_file(save_path,label,file):
    status=validate_file(file)  
    if(status != "ok"):
        return status 
    else:
        encoding = get_face_encodings(file_path=file)
        if(type(encoding)=="str"):
            return encoding  #Error message
        else:
            save_new_encoding(save_path,[encoding],label)
            return "facelock: Successfully added Face to Records"


def add_face_via_capture(save_path,label):
    known_face_encodings,known_face_names=[],[]
    face_locations = []
    face_encodings = []
    face_names = []
    encoding=[]
    known_face_encodings,known_face_names = get_recorded_data(save_path)
    
    # print(known_face_names)
    

    if(label in known_face_names):
        print("facelock: Given Label Already in Records")
        return
    cam = cv2.VideoCapture(0)
    screen_res = (1280,720)
    
    cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow("Camera", screen_res[0] - 1, screen_res[1] - 1)
    cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    alternate = False
    while True:
        _,frame = cam.read()
        resized_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = resized_frame[:, :, ::-1]
        if(alternate):
            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations,model="small")

            face_names = []
            for face_encoding in face_encodings:
                
                matches = fr.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
                name = "Unknown"
    
                if(len(known_face_encodings) !=0):
                    face_distances = fr.face_distance(known_face_encodings, face_encoding)
                    best_match_index = argmin(face_distances)
                    # print("argmin index",best_match_index)
                    # print(matches)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
    
                face_names.append(name)
        
        alternate = not alternate
    
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            left-=5
            top-=5
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
    
            cv2.rectangle(frame, (left,top-20), (right, top), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX 
            cv2.putText(frame, name, (left + 6, top-5), font, 0.5, (255, 255, 255), 1)
            if("Unknown" not in face_names):
                cv2.putText(frame, "All Detected Faces are registered",\
                            (50,50), font, 0.75, (255,255,255))
            elif(face_names.count("Unknown") > 1):
                cv2.putText(frame, "More than 1 unknown faces. Need only one",\
                            (50,50), font, 0.75, (255,255,255))
            else:
                i = face_names.index("Unknown")
                encoding = face_encodings[i]
                cv2.putText(frame, "Face Recorded. Press Q to Quit",\
                            (50,50), font, 1, (255,255,255))
        frame = cv2.resize(frame,screen_res)
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cam.release()
    cv2.destroyAllWindows()
    # print("save encoding : ",encoding)
    if(len(encoding)!=0):   
        save_new_encoding(save_path, [encoding], label)
        print(f"Face with label {label} saved Successfully")
    
    



def add_face(save_path,label,file=None):
    if(file == None):
        add_face_via_capture(save_path,label)
    else:
        add_face_via_file(save_path,label,file)
        
    return 1


