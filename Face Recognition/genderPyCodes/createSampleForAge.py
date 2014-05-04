'''
prepare frontal face images to be passed to fisherBased.py
 
- find eyes using HAAR wavelet based detection (Viola-Jones method)
- image registration
    - rotate the image so that line joining the centers of the eyes
      is horizontal
    - translate and scale so that all images are in same coordinate system 
'''
import cv2
import imgUtils
import registerImage
import os

# Assume supplied images have single, frontal face
sourcePath = '/Users/pradeep/Desktop/Hackathon/Face Recognition/trainFaces/teen/' 
filePaths, fileNames = imgUtils.fetchFiles(sourcePath, 'ENDS_WITH', '.jpg')

#print filePaths[:5]
#print fileNames[:5]

# faceCasc = imgUtils.chooseCascade(choice='frontalFace')
eyeCasc = imgUtils.chooseCascade(choice='eyeGlasses') # left one ins't always first in returned list
    
sz = 94
offSetH = 0.25
offSetV = 0.25

for path, name in zip(filePaths,fileNames):
    # Load image in single channle grayscale
    img = cv2.imread(path,0)
    
    # Register the image with alignment at eyes
    #img = registerImage.alignAtEyes(eyeCasc, img, name, sz, offSetH,offSetV)

    # Images are already aligned so only resize
    img = cv2.resize(img,(sz,sz),interpolation=cv2.cv.CV_INTER_AREA)
    
    if img is None:
        print 'could not align ' + name
    else:
        # newName and save
        if name.startswith('AM') or name.startswith('BM') or name.startswith('m'):
            dstPath = '/Users/pradeep/Desktop/Hackathon/Face Recognition/trainFaces/teen/males94/'
        else:
            dstPath = '/Users/pradeep/Desktop/Hackathon/Face Recognition/trainFaces/teen/females94/'
         
        newName = dstPath + os.path.splitext(name)[0] + '.jpg'
        cv2.imwrite(newName, img)
    
print 'finished creating samples'