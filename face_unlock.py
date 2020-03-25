from sys import exit
import os
from util import load
from model import FaceRecognizer
save_path = "/etc/facelock/face_records/"
save_file = save_path+"database.pkl"

if(os.path.exists(save_file)):
    recognizer = load(save_file,train=False)
    if  recognizer.no_known_faces == 0:
        print("facelock: No saved records")
        exit(2)
    else:
        recognizer.train_recognizer()
        recognizer.authenticate_face()
        
else:
    print("facelock: No saved records")
    exit(2)


