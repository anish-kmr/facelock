from model import FaceDetector,FaceRecognizer
from util import save,load
import argparse
import os

base_path = "/etc/facelock/"
save_path = base_path+"face_records/"
save_file = save_path+"database.pkl"
authentication_shfile = base_path+"face_authenticate.sh"
pam_config = f"auth sufficient pam_exec.so stdout debug {authentication_shfile}\n"
comment = "#Face Authentication Script\n"
if(os.path.exists(save_file)):
    recognizer = load(save_file,train=False)
else:
    recognizer = FaceRecognizer()
    
def adder(args):
    added = recognizer.add_face(args.label)
    if not added:
        print(f"facelock : Specified label '{args.label}' already exists.")
        print(f"Do You want to add more faces to label '{args.label}'.")
        print("Hint: Adding more faces to a label will help recognize faces easily.")
        while True:
            choice = input("Enter [y/n]: ")
            if(choice == "y" or choice == "Y" ):
                recognizer.add_more_faces(args.label)
                save(recognizer, save_file)
                return
            elif(choice == "n" or choice == "N"):
                return
            else:
                print("facelock : Please enter 'y' or 'n' ")
    else:
        save(recognizer, save_file)
            
def list_labels(args):
    face_list = recognizer.list_faces()
    if len(face_list)>0:
        print("facelock: Recorded Face Labels are : ")
        for i,key in enumerate(face_list):
            print(f"{i+1}.{key}({face_list[key]} faces)")
    else:
        print("facelock: No Faces in Record :")
        print("facelock: Try 'facelock add <your_label>' to add a new face to records")

def remover(args):
    label=args.label
    
    if  len(recognizer.labels_map)==0:
        print("facelock: No saved records")
    elif (len(recognizer.labels_map)==1 and status(printing=False)):
        print("facelock: Only 1 Face in record. Disable Facelock authentication first, then remove labels ")
        return
    else:
        removed = recognizer.remove_face(label)
        if(not removed):
            print(f"facelock: {label} is not in the saved records.")
            return
        else:
            save(recognizer, save_file)
            print(f"facelock: {label}({removed} faces) removed from records.")
            

def enable(args):
        
    if  recognizer.no_known_faces==0:
        print("facelock: No saved records")
        print("facelock: Add at least one face to record by 'facelock add <your_label>'")
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

def test(args):
    recognizer.train_recognizer()
    recognizer.test_recognizer()
    
parser = argparse.ArgumentParser(prog="Facelock",usage="A command line tool for faclock in linux. ")

subparsers = parser.add_subparsers(description="Use these subcommands to change configurations of facelock")

add = subparsers.add_parser("add",help="Add a new face  for authentications.\n (For more: 'facelock add -h') ")
add.add_argument("label", help="Label for the face")
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

test_parser = subparsers.add_parser("test", help="Test the Facelock Recognizer")
test_parser.set_defaults(func=test)

args = parser.parse_args()
args.func(args)
