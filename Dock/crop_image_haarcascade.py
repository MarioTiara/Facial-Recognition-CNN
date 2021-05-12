import glob
from PIL import Image
import cv2
import numpy as np

count=0
image_list=[]

face_classifier = cv2.CascadeClassifier("/home/mario/Pyhton_workspace/image preprocessing/Haarcascade/haarcascade_frontalface_default.xml")

def face_cropped(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    if faces is ():
        return None
    for (x,y,w,h) in faces:
        cropped_face = img[y:y+h,x:x+w]
    return cropped_face


for fileName in glob.glob("/home/mario/Pyhton_workspace/image preprocessing/data mentah/*.jpg"):
    img=Image.open(fileName)
    image_list.append(img)

for image in image_list:
    image=np.array(image)
    face_target=face_cropped(image)
    if face_target is not None:
        face=cv2.resize((face_target),(224,224))
        #print(face)
        label="data/"+str(count)+".jpg"
        cv2.imwrite(label,face)
        count+=1
        print(count)
        
    
