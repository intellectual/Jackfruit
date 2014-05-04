'''
Cognition phase requires patterns i.e. signals to be inputted to the cognizer

A dictionary is then built in which labels are assigned to incoming patterns
 - in supervised learning these assignments are done by another cognizer
 - in unsupervised learning the cognizer makes use of "innate" labels
   but philosophically, there isn't a way to explain unsupervised learning
   because that which built the cognizer (society, ecology, selection, God, etc.) 
   is its supervisor and thereby all learning is supervised learning. 
   
The cognizer then trains on i.e. memorizes the pattern-label mappings

In recognition phase a new pattern without a label is given 
 - the cognizer compares it with existing mappings 
 - and then assigns a label to it. 
 
The process of comparing patterns and assigning a label to the new one 
is called classification. A classifier includes a:
  - technique for determining "distance" between the compared patterns
    - e.g. euclidean, manhattan, cosine, etc. These techniques have a variety
      of parameters which yield profoundly different meaning of "distance"
  - notion of "threshold" on the distance which determines 
    - if the new pattern Ny is close enough to memorized pattern Kx,
      the label of Kx is assigned to Ny
      else, a new label or a generic label of "unrecognized" is assigned to Ny
  - technique for generating a new label for unrecognized patterns

The distance between the patterns Ny and Kx is called the "error"
    
The recognition phase can be repeated with different values of distance and threshold.
Additionally, a method can be constructed which determines how the different values of 
the criteria are obtained for subsequent repetitions along with another criterion on
the number of repetitions. This process of feeding the output of one iteration of 
recognition phase to the next is called cascading or chaining. In each cascade, the 
cognizer is likely to "forget" the outcome of the previous cascade i.e. the new 
encodings overwrite previous encodings in a destructive manner, but the overall process
is constructive (more appropriately termed as generative). 

Some of the methods of classifiers and ways to cascading them are:
 - Error maximization

 - Error minimization
   - Mean squareroot error of a distance
     - k-NearestNeighbors
     - k-NearestMeans
   - Logarithmic error of a distance
     - adaBoost 
 
 The following error minimization methods
 can be used with any combination of distance metric
 - artificial neural networks 
 - support vecotor machine
 - gradient search
 - self organizing maps

By installing a "feedback loop" the existing architecture of the cognizer can be 
utilized for creating subsequent iterations of the recognition phase (cascading).
In each iteration, the existing architecture attains minute changes and the type of 
feedback loop used may generate a criterion for terminating the iterations. 
An artificial neural network typically involves feedback loops. In practice, the 
environment in which a cognizer exists constructs a feedback loop for the cognizer. 

Each method of cascading and technique for generating criteria have their peculiarities.
   
Conclusion:
A cognizer has an architecture for the functions of:
 - cognition which, involves acceptance of arbitrary changes within the cognizer's 
   overall architecture that do not destroy the cognizer
 - recognition which, involves encoding a new, arbitrary change, to the outcome of a
   previous change within the cognizer's architecture
   
Eventually the new changes are not entirely "arbitrary" for they match with a dictionary 
and the encodings within the dictionary have knowledge about future changes that the cognizer
may experience. This knowledge can be utilized to trigger changes within the cognizer's "inventory". 

The cognizer's inventory is the collection of all tangible entities which the cognizer 
can observer and control. However, the caveat is that the cognizer is within the inventory 
of that which created it and thereby it may not have sufficient ability to observer nor control 
its inventory for its creator didn't or couldn't instill such functionality into it. 
'''

import cv2
import imgUtils
from facerec import feature, distance, classifier, model

# Extract ideal patterns from within the given raw patterns
# Fishfaces is a cascading of Principle Component Analysis
# and Linear Discriminate Analysis
featureExtractor = feature.Fisherfaces()

# Type of distance should match classifier
distance = distance.EuclideanDistance()

# Type of classifier and criterion for selection
classifier = classifier.NearestNeighbor(dist_metric=distance, k=3)

# The overall architecture
predictor = model.PredictableModel(featureExtractor,classifier)
 
# The training patterns
# these patterns were preprocessed via createSample.py 
# with sz=210, offSetH = 0.25 and offSetV = 0.25
filePaths, fileNames = imgUtils.fetchFiles('/Users/pradeep/Desktop/Hackathon/Face Recognition/trainFaces/ageTraining/', 
                                           'ENDS_WITH', 
                                           'proto.jpg')

# Labels of the raw patterns 
X = []
y = []
for path, name in zip(filePaths,fileNames):
    img = cv2.imread(path,0) 
    X.append(img)
    
    if name.endswith('tNES_proto.jpg'):
        y.append(0) # feminie
    else:
        y.append(1) # masculine

# Train on the samples and corresponding labels
predictor.compute(X,y)

# pickle the predictor
imgUtils.savePredictor('gendClassify_fisherFace_ED_k3_youngFaces.pkl', predictor)

print 'Load the predictor into another python module with cPickle to use it'
