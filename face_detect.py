#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:46:07 2020

@author: chandan
"""
from face_recognition import face_locations,face_encodings,load_image_file

def get_face_encodings(file_path=None,image=None):
    if(file_path != None):
        image = load_image_file(file_path)
    
    faces = face_locations(image)
    length = len(faces)
    if(length > 1):
        return "facelock: More than One faces found. One Face at a time only"
    elif(length==0):
        return "facelock: No Faces Found"
    else:
        encoding = face_encodings(image,faces)[0]
        return encoding
        
    
