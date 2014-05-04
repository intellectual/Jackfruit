import numpy
from registerImage import alignAtEyes
from cv2 import CascadeClassifier, VideoCapture, cvtColor, COLOR_BGR2GRAY, rectangle, putText, imshow, waitKey, destroyAllWindows
from cv2.cv import CV_HAAR_SCALE_IMAGE, CV_FONT_HERSHEY_DUPLEX, CV_HAAR_DO_CANNY_PRUNING
from cPickle import load as cpload
import sys
import os
from Jackfruit import insert_into_mongo
import datetime


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

# Checks for pyinstaller
if getattr(sys, 'frozen', False):
    # we are running in a PyInstaller bundle
    basedir = sys._MEIPASS
    #print 'sys._MIEPASS: ' + basedir
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)
    
        
def findFace(img,FaceCasc):
    # Make sure that img is frontal face
    faceRegion = faceCasc.detectMultiScale(img,scaleFactor=1.2,minNeighbors=3,minSize=(40,40),flags=CV_HAAR_SCALE_IMAGE)
    if len(faceRegion) > 1:
        _imgs = []
        for region in faceRegion:
            x, y, w, h = region
            w += int(w/8)
            h += int(h/8) # to accomodate chin 
            imgCrop = img[y:y+h,x:x+w]
            
#             imshow('faceDetection', imgCrop) 
#             waitKey()
#             destroyAllWindows()
            
            _imgs.append(imgCrop)
        return _imgs, faceRegion
    elif len(faceRegion) == 1:
        try:
            x, y, w, h = faceRegion[0]
            w += int(w/8)
            h += int(h/8) # to accomodate chin 
            _img = img[y:y+h,x:x+w]
            return [_img], faceRegion
        except ValueError:
            return None, None
    else:
        return None, None
            

# load the trainedPredictor 
pklFile = open(os.path.join(basedir,'pklFiles/gend_fisher_ED_k3_youngFaces_25Nov2013.pkl'), 'rb')
trainedPredictor = cpload(pklFile)
pklFile.close()

# The img source
capture = VideoCapture(0)
name = 'cameraScene'

# HAAR cascades for face and eyes
faceCasc = CascadeClassifier(os.path.join(basedir,'cascadeFiles/haarcascade_frontalface_alt2.xml'))
eyeCasc = CascadeClassifier(os.path.join(basedir,'cascadeFiles/haarcascade_eye_tree_eyeglasses.xml'))

gender1 = 0
gender2 = 0
count = 0

# Important parameters for alignAtEyes()    
sz = 210
offSetH = 0.25
offSetV = 0.25

keyPressed = -1
while(keyPressed != 27):
    unused_retval, img0 = capture.read()
    
    img1 = cvtColor(img0, COLOR_BGR2GRAY)
    
    faceImgs, faceRegions = findFace(img1,faceCasc)
    
    if faceImgs is None:
        pass
    else:
        for indx, img in enumerate(faceImgs):
            # Register the image with alignment at eyes
            img = alignAtEyes(eyeCasc, img, name, sz, offSetH, offSetV)
            
            # Get prediction and draw on img0
            if img is None:
                pass
#                 print 'could not align faceRegion {0} in {1}'.format(indx,name)
            else:
                prediction = trainedPredictor.predict(img)
                predictResult = prediction[0]
                
                if predictResult == 0:
                    gender = 'female'
                    fontColor = (250,250,250)
                    gender2 = gender2+1
                else:
                    gender = 'male'
                    fontColor = (250,250,250)
                    gender1 = gender1+1

                count = gender1 + gender2

                dt = datetime.datetime.now()
                time_milli_secs = unix_time(dt)

                json = {'timestamp' : time_milli_secs, 'gender' : gender, 'count' : count, 'gender1' : gender1, 'gender2' : gender2}

                insert_into_mongo(json)

                
                x1, y1, w1, h1 = faceRegions[indx]
                rectangle(img0,
                          (x1,y1),
                          (x1+w1,y1+h1),
                          (100,255,0),2)
                putText(img=img0,
                            text='Gender: ' + gender,
                            org=(x1,y1+h1-10),
                            fontFace=CV_FONT_HERSHEY_DUPLEX,
                            fontScale=0.75,
                            color=fontColor)
                
    imshow('appDemo', img0) 
    keyPressed = waitKey(2)
destroyAllWindows()
capture.release()

