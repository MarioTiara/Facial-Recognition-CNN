#import Libraries
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from tensorflow.keras.preprocessing.image import img_to_array,load_img

import cv2
import numpy as np
from datetime import datetime
from firebase import sendFirebase

#import functions
from main_window import *
import CNN_predict

class MainWindow(QtWidgets.QMainWindow):
    # class constructor
    def __init__ (self, parent=None):
        # call QWidget constructor
        super(MainWindow, self).__init__(parent=parent)
        self.counter=[0,0,0]
        self.lblConf=0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model=CNN_predict.Model()
        self.status="STATUS"
        self.classes = ['Aji Arya Dewangga','Mario Tiara Pratama','Unknown']
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
        self.now = datetime.now()
        self.dt_string =self.now.strftime("%B %d, %Y %H:%M:%S")
        self.Data={"Nama": "Mario", "Waktu" : self.dt_string}

        if self.face_cascade.empty():
            QMessageBox.information(self, "Error Loading cascade classifier" , "Unable to load the face	cascade classifier xml file")
            sys.exit()
        # creat timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.detectFaces)
        # Connect control_bt to controlTimer
        self.ui.control_bt.clicked.connect(self.controlTimer)

    # detect face
    def detectFaces(self):
        # read frame from video capture
        ret, frame = self.cap.read()
        
        
        # resize frame image
        scaling_factor = 0.8
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
                # convert frame to GRAY format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect rect faces
        face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # for all detected faces
        for (x, y, w, h) in face_rects:
            # draw green rect on face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            faces = frame[y:y + h, x:x + w]
            face = cv2.resize(faces, (200,200))
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            Y = y-10 if y-10>10 else y+10

            cv2.imwrite('data/captured/face.jpg', gray)
            
            img=load_img('data/captured/face.jpg',target_size=(200,200))
            img=img_to_array(img)
            img = np.expand_dims(img, axis=0)
            
            conf = self.model.predict(img)
            print(conf[0])

            idx = np.argmax(conf[0])
            label = self.classes[idx]

            if (idx==0):
                self.lblConf=conf[0][0]
                self.counter[1]=0
                self.counter[2]=0
                self.counter[0]=self.counter[0]+1
                print("counter[0]:"+str(self.counter[0]))
                if (self.counter[0]>=3):
                    self.Data["Nama"]=label
                    directory="No"+str(self.counter[0]-2)
                    sendFirebase(self.Data,label,direcNo) 

            elif(idx==1):
                self.lblConf=conf[0][1]
                self.counter[0]=0
                self.counter[2]=0
                self.counter[1]=self.counter[1]+1

                print ("counter[1]:"+str(self.counter[1]))
                if (self.counter[1]>=3):
                    self.Data["Nama"]=label
                    direcNo="No"+str(self.counter[1]-2)
                    sendFirebase(self.Data,label,direcNo) 

            elif (idx==2):
                self.lblConf=conf[0][2]
                self.counter[0]=0
                self.counter[1]=0 
                self.counter[2]=self.counter[2]+1
                print("counter[2]:"+str(self.counter[2]))
                if (self.counter[2]>=3):
                    self.Data["Nama"]=label
                    direcNo="No"+str(self.counter[2]-2)
                    sendFirebase(self.Data,label,direcNo)


            if (conf[0][0]<0.5 and conf[0][1]<0.5 and conf[0][2]<0.5 ): 
                label=self.classes[2]
                self.counter[0]=0
                self.counter[1]=0 
                self.counter[2]=self.counter[2]+1
                print("counter[2]:"+str(self.counter[2]))
                if (self.counter[2]>=3):
                    self.Data["Nama"]=label
                    direcNo="No"+str(self.counter[2]-2)
                    sendFirebase(self.Data,label,direcNo)    

            ConfLvl=self.lblConf*100
            ConfLvl_lbl="{:.2f}".format(ConfLvl) + "%"
            lbl=label+"("+ConfLvl_lbl+")"
            
            cv2.putText(frame, lbl, (x, Y),  cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
            
            self.ui.name_lbl.setText("Name: " + label)

            if (label==self.classes[2]): self.status="INVALID"
            else:self.status="VALID"
            self.ui.Sts_lbl.setText(self.status)

           
            self.ui.time_lbl.setText("Time :"+ self.dt_string)
            
            
            
        # convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # get frame infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from RGB frame
        #gray_flip = cv2.flip( frame ,1)
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        self.ui.img_lbl.setPixmap(QPixmap.fromImage(qImg))     
        

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
