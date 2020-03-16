#!/usr/bin/env python3
from face_add import add_face
from face_records import get_recorded_data,save_recorded_data
import argparse
from numpy import ndarray,where,delete

base_path = "/etc/facelock/"
save_path = base_path+"face_records/"
authentication_shfile = base_path+"face_authenticate.sh"
log_dir = base_path+"logs/"
pam_config = f"auth sufficient pam_exec.so log={log_dir}facelock_logs.log debug {authentication_shfile}\n"
comment = "#Face Authentication Script\n"
def adder(args):
    add_face(save_path,args.label,args.file)
    

def list_labels(args):
    _,labels = get_recorded_data(save_path)
    if len(labels)>0:
        print("facelock: Recorded Face Labels are : ")
        for i in range(len(labels)):
            print(f"{i+1}. {labels[i]}")
    else:
        print("facelock: No Faces in Record :")
        print("facelock: Try 'facelock add <your_label>' to add a new face to records")

def remover(args):
    label=args.label
    known_face_encodings,known_face_names =  get_recorded_data(save_path)
    if  len(known_face_encodings)==0:
        print("facelock: No saved records")
    else:
        
        label_index,  = where(known_face_names==label)
        if(len(label_index)==0 ):
            print(f"facelock: {label} is not in the saved records.")
            return
        else:
            if(len(known_face_names)==1 and status(printing=False)):
                print("facelock: Only 1 Face in record. Disable Facelock authentication first, then remove labels ")
                return
            known_face_encodings=delete(known_face_encodings,label_index,0)
            known_face_names=delete(known_face_names,label_index,0)
            save_recorded_data(save_path, known_face_encodings,known_face_names)
            print(f"facelock: {label} removed from records.")
            

def enable(args):
        
    known_face_encodings,known_face_names =  get_recorded_data(save_path)
    if  len(known_face_encodings)==0:
        print("facelock: No saved records")
        print("facelock: Add at least one face to record by 'facelock add <your_label>' or facelock add <your_label> --file='/path/to/faceimage.jpg'")
        return False
        

    with open("/etc/pam.d/common-auth","r") as f : content = f.readlines()
    com_found,com_index = False,-1
    for i in range(len(content)):
        if(content[i]==comment):
            com_found=True
            com_index = i
        if(content[i]==pam_config):
            break    
    else:    
        
        with open("/etc/pam.d/common-auth",'w') as f :
            if(com_found):
                f.writelines(content[:com_index+1])
                f.write(pam_config+"\n")
                f.writelines(content[com_index+2:])
            else:
                f.writelines([comment,pam_config+"\n"])
                f.writelines(content)
        print("facelock: Facelock Authentication Enabled")

def disable(args):
    with open("/etc/pam.d/common-auth","r") as f : content = f.readlines()
    com_found,com_index = False,-1
    pam_found,pam_index = False,-1
    for i in range(len(content)):
        if(content[i]==comment):
            com_found=True
            com_index = i
        if(content[i]==pam_config):
            pam_found=True
            pam_index = i
    
    with open("/etc/pam.d/common-auth",'w') as f :
        if(pam_found):
            f.writelines(content[:com_index])
            f.writelines(content[com_index+1:pam_index])
            f.writelines(content[pam_index+1:])
            print("facelock: Facelock Authentication Disabled")
        elif(com_found):
            f.writelines(content[:com_index])
            f.writelines(content[com_index+1:])
            print("facelock: Facelock Authentication Already Disabled")
        else:
            f.writelines(content)
            print("facelock: Facelock Authentication Already Disabled")
        

def status(printing=True):
    with open("/etc/pam.d/common-auth","r") as f : content = f.readlines()
    pam_found = False
    for i in range(len(content)):
        if(content[i]==pam_config):
            if(printing):
                print("facelock: Facelock Authentication is Enabled")
            return True
    else:
        if(printing):
            print("facelock: Facelock Authentication is Disabled")
        return False

parser = argparse.ArgumentParser(prog="Facelock",usage="A command line tool for faclock in linux. ")

subparsers = parser.add_subparsers(description="Use these subcommands to change configurations of facelock")

add = subparsers.add_parser("add",help="Add a new face  for authentications.\n (For more: 'facelock add -h') ")
add.add_argument("label", help="Label for the face")
add.add_argument("--file",help="Path of image containing face")
add.set_defaults(func=adder)



remove = subparsers.add_parser("remove",help="Remove an existing face by label from records.\n (For more: 'facelock remove -h')")
remove.add_argument("label", help="Name of face label to be removed")
remove.set_defaults(func=remover)

labels = subparsers.add_parser("list",help="List all Faces which can pass Facelock authentication.")
labels.set_defaults(func=list_labels)

enable_parser = subparsers.add_parser("enable",help="Enable Facelock Authentication.")
enable_parser.set_defaults(func=enable)

disable_parser = subparsers.add_parser("disable",help="Disable Facelock Authentication.[This does not resets previous face records.]")
disable_parser.set_defaults(func=disable)

status_parser = subparsers.add_parser("status",help="Check if Facelock Authentication is Enabled or Disabled")
status_parser.set_defaults(func=status)

args = parser.parse_args()
args.func(args)
