import cv2
import numpy as np
class FaceDetector:
    def __init__(self):
        base_path = "/etc/facelock/"
        prototxt_path = base_path + "deploy.prototxt"
        caffemodel_path = base_path + "res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path,caffemodel_path)
        
    def detect(self,image):
        
        faces=[]
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,(300, 300),(104.0,177.0, 123.0))
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
        
            if confidence >0.5:
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = image[startY:endY,startX:endX,:]
                if(face.shape[0] <= 32 or face.shape[1]<=32):
                    continue
                else:
                    face = cv2.resize(face, (180,180))
                    faces.append((face,(startX,startY,endY-startY,endX-startX)))
        return faces

class FaceRecognizer:
    def __init__(self): 
      
        self.faces_dataset=[]
        self.labels_id=[]
        self.labels_map=[]              
        self.no_known_faces=0
        self.detector = FaceDetector()
        self.model = cv2.face.LBPHFaceRecognizer_create(threshold=55)
        # print(f"#Known Faces : {self.no_known_faces}")
    
    def train_recognizer(self):
        self.model.train(self.faces_dataset,np.array(self.labels_id))
        
    def add_face(self,label,id=None):
        if(label in self.labels_map):
            return 0
        v = cv2.VideoCapture(0)
        screen_res = (1280,720)
        cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Camera", screen_res[0] - 1, screen_res[1] - 1)
        cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            _,frame = v.read()
            faces = self.detector.detect(frame)
            for face,(x,y,h,w) in faces:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                self.faces_dataset.append(face)
                self.labels_id.append(self.no_known_faces)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2)
            frame = cv2.resize(frame,screen_res)
            cv2.imshow("Camera",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        v.release()
        cv2.destroyAllWindows()
        self.labels_map.append(label)
        self.no_known_faces+=1
        self.train_recognizer()
        
        return 1
    
    def add_more_faces(self,label):
        try:
            id = self.labels_map.index(label)
        except ValueError:
            return False
        
        v = cv2.VideoCapture(0)
        while True:
            _,frame = v.read()
            faces = self.detector.detect(frame)
            for face,(x,y,h,w) in faces:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                self.faces_dataset.append(face)
                self.labels_id.append(id)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),1)
            cv2.imshow("Video",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        v.release()
        cv2.destroyAllWindows()
        self.train_recognizer()
        return True
    
    def remove_face(self,label):
        try:
            id = self.labels_map.index(label)
        except ValueError:
            return False
        deleted,i=0,0
        n=len(self.labels_id)
        print("len : ",n,"id :",id)
        while i < n:
            if( self.labels_id[i]==id ):
                del self.labels_id[i]
                del self.faces_dataset[i]
                deleted+=1
                n-=1
        del self.labels_map[id]
        self.no_known_faces-=1
        if(len(self.labels_map) > 0 ):
            self.train_recognizer()
        return deleted
    
    def list_faces(self):
        face_list = { label:self.labels_id.count(i) for i,label in enumerate(self.labels_map)}
        return face_list
    
    def test_recognizer(self):
        v = cv2.VideoCapture(0)
        screen_res = (1280,720)
        cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Camera", screen_res[0] - 1, screen_res[1] - 1)
        cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            _,frame = v.read()
            faces = self.detector.detect(frame)
            for face,(x,y,h,w) in faces:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                id,distance = self.model.predict(face)
                if(id in self.labels_id):
                    name = self.labels_map[id]
                else:
                    name="Unknown"
            
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),1)
                cv2.rectangle(frame, (x,y-20), (x+w,y), (255,0,0),-1)
                cv2.putText(frame, name, (x,y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255,255), 1)
            frame = cv2.resize(frame,screen_res)
            cv2.imshow("Camera",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        
        v.release()
        cv2.destroyAllWindows()
    
    def authenticate_face(self):
        v = cv2.VideoCapture(0)
        passed=False
        while True:
            _,frame = v.read()
            faces = self.detector.detect(frame)
            for face,(x,y,h,w) in faces:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                id,distance = self.model.predict(face)
                if(id in self.labels_id):
                    name = self.labels_map[id]    
                    print(f"facelock: Authenticated by {name}")
                    passed = True
                    break
            if passed:
                break
        v.release()
        cv2.destroyAllWindows()
