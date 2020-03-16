# Facelock

Now use your face for login,sudo commands and other authentications on linux

### Prerequisites

1. Python3
2. Python Modules:
   - Numpy
   - OpenCV
   - Dlib
   - face_recognition 
     
You can either install these dependencies seperately yourselves or by running this:
```
$ cd facelock/
$ chmod +x requirements.sh && ./requirements.sh
```
This can take a while

### Installing
Clone the repositery whwerever you like
```
git clone https:/github.com/anish-kmr/facelock.git
```
cd into cloned repo

```
cd facelock
```
and install the facelock
```
chmod +x install.sh && ./install.sh
```

## Running
Check the status of facelock
```
$ facelock status
```
First time, it should say disabled.
#### Add Faces
You can add faces which can unlock facelock by either an image containing only your photo or by capturing by videocam.
- Using Image file
```
$ facelock add your_label --file="path/to/image.jpg"
```
- Using Webcam 
```
$ facelock add your_label 
```
Change your_label to your name or whatever you like.

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
