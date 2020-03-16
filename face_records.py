#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 22:19:35 2020

@author: chandan
"""
from numpy import load,savez_compressed,ndarray,vstack
from os.path import exists

def save_new_encoding(save_path,encoding,label):
    save_file = save_path + "face_records.npz"
    if(exists(save_file)):
        data = load(save_file,allow_pickle=True)
        known_encodings,known_labels = data['arr_0'],data['arr_1'].tolist()
        if(label in  known_labels):
            print("facelock: Given Label Already registered in records")
            return
        # print("shape ",known_encodings.shape,"enc shape: ",encoding.shape)
    else:
        known_encodings,known_labels = [],[]    
    
    if(len(known_encodings)==0):
        known_encodings = []
        known_encodings.extend(encoding)
    else:
        # print("shape ",known_encodings.shape,"enc shape: ")
        known_encodings=vstack((known_encodings,encoding))
    known_labels.append(label)
    
    savez_compressed(save_file,known_encodings,known_labels)
    
    return True

def save_recorded_data(save_path,encodings,labels):
    save_file = save_path + "face_records.npz"
    savez_compressed(save_file,encodings,labels)
    return True
def get_recorded_data(save_path):
    if(exists(save_path+"face_records.npz")):
        data = load(save_path+"face_records.npz",allow_pickle=True)
        encodings,labels = data['arr_0'],data['arr_1']
        return (encodings,labels)
    else:
        return ([],[])