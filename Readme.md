# Facelock

Now use your face for login,sudo commands and other authentications on linux. 


### Requirements

1. Python3.6 or above
2. Python Modules:
   - numpy
   - opencv-python
   - opencv-contrib-python
     

### Installing
### Step 1

Clone the repositery wherever you like
```
git clone https://github.com/anish-kmr/facelock.git
```
Rename from 'facelock-master' to 'facelock' and
cd into cloned repo

```
$ cd facelock
```
### Step 2
**If you have all requirements listed above installed ,then you can leave this step.**
```
$ chmod +x requirements.sh
$ ./requirements.sh
```
This can take a while
 
 ### Step 3
Install  facelock
```
$ chmod +x install.sh 
$ ./install.sh
```

You now have facelock installed

## Running
Check the status of facelock
```
$ facelock status
```
First time, it should say disabled.
#### Add Faces
You can add faces facelock by webcam.
```
$ facelock add your_label 
```
Change 'your_label' to your name or whatever you like.<br>
This will open your webcam. Show your face to webcam for a few seconds at different distances.

#### Test Facelock
To check whether you are recognized or not ,type this:
```
$ facelock test
```
Your label should appear on top of your face.
If not, try adding more of your faces to database by 'facelock add <your_existing_label>' 
#### Enable Facelock
```
$ facelock enable
```
By doing this, every time you are asked to write password ,your face will be scanned and used to unlock instead.<br>
Note that if your face is not scanned within 2min it will ask for the password.

#### List Face Labels
To see who all can pass facelock 
```
$ facelock list
```
The labels listed were set by you when you added them.

#### Remove Faces
To remove faces from facelock records, 
```
$ facelock remove label_to_delete
```
'label_to_delete' being the label name you want to delete

#### Disable Facelock
```
$ facelock disable
```
