import pickle
import cv2
from model import FaceDetector

def save(rec,file):
    rec.detector = None
    rec.model = None
    with open(file,"wb") as f:
        pickle.dump(rec,f)
    print("saved")

def load(file,train=True):
    with open(file,'rb') as f:
        rec = pickle.load(f)
    rec.model = cv2.face.LBPHFaceRecognizer_create(threshold=55)
    rec.detector = FaceDetector()
    if(train):
        rec.train_recognizer()
    return rec
