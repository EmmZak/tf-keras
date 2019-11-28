from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer
import cv2
import sys
from datetime import datetime
import os
from threading import Thread
from time import time, sleep
import glob
import numpy as np
import tensorflow.keras
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from time import time
import plc

##############################################################################################
cam = cv2.VideoCapture(0)
np.set_printoptions(suppress=True)
#####################################################################################" model "
model = tensorflow.keras.models.load_model('converted_keras/keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
classes = open("converted_keras/labels.txt").readlines()
#####################################################################################" model "

app = QtWidgets.QApplication([])
dlg = uic.loadUi("detect.ui")

def setLabel1(n):
    """
    if n == 0:
        dlg.pet1.setStyleSheet('QLabel#pet1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.glass1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.pet1.setStyleSheet('')
        dlg.glass1.setStyleSheet('')

    if n == 1:
        dlg.pet1.setStyleSheet('QLabel#pet1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.glass1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.pet1.setStyleSheet('')
        dlg.glass1.setStyleSheet('')

    if n == 2:
        dlg.acier1.setStyleSheet('QLabel#acier1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.alu1.setStyleSheet('QLabel#can1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.acier1.setStyleSheet('')
        dlg.alu1.setStyleSheet('')

    if n == 3:
        dlg.pet1.setStyleSheet('QLabel#pet1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.glass1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.pet1.setStyleSheet('')
        dlg.glass1.setStyleSheet('')

    if n == 4:
        dlg.pet1.setStyleSheet('QLabel#pet1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.glass1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.pet1.setStyleSheet('')
        dlg.glass1.setStyleSheet('')
    """
    if n == 5:
        dlg.acier1.setStyleSheet('QLabel#acier1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.pp1.setStyleSheet('QLabel#pp1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.acier1.setStyleSheet('')
        dlg.pp1.setStyleSheet('')
    
    metal = plc.getCoil("metal")
    if metal == True:
        dlg.metal.setStyleSheet('QLabel#metal {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.acier2.setStyleSheet('QLabel#acier2 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.finalres.setText("Acier")
        dlg.finalres.setStyleSheet('QLabel#finalres {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.metal.setStyleSheet('')
        dlg.acier2.setStyleSheet('')
        dlg.finalres.setText("Nothing")
        dlg.finalres.setStyleSheet('')

    verre = plc.getCoil("verre")
    if verre == True:
        dlg.cap.setStyleSheet('QLabel#cap {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.cap.setStyleSheet('')

    """
    if metal == True:
        dlg.acier2.setStyleSheet('QLabel#acier2 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.cap.setStyleSheet('QLabel#cap {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.finalres.setText("Acier")
        dlg.finalres.setStyleSheet('QLabel#finalres {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.acier2.setStyleSheet('')
        dlg.cap.setStyleSheet('')
        dlg.finalres.setText("Nothing")
        dlg.finalres.setStyleSheet('')

    if n == 6:
        dlg.filme1.setStyleSheet('QLabel#filme1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.alu1.setStyleSheet('QLabel#alu1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
    else:
        dlg.filme1.setStyleSheet('')
        dlg.alu1.setStyleSheet('')
        dlg.finalres.setText("Nothing")
        dlg.finalres.setStyleSheet('')
    """

def setLabel2(n, label):

    if n == 5:
        dlg.label.setStyleSheet('QLabel#acier1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')

def setMetalCap():

    metal = plc.getCoil("metal")

    if metal == True:
        dlg.metal.setStyleSheet('QLabel#metal {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.nonmetal.setStyleSheet('')
    else:
        dlg.nonmetal.setStyleSheet('QLabel#nonmetal {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.metal.setStyleSheet('')
    
    verre = plc.getCoil("verre")

    if verre == True:
        dlg.cap.setStyleSheet('QLabel#cap {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.noncap.setStyleSheet('')
    else:
        dlg.noncap.setStyleSheet('QLabel#noncap {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        dlg.cap.setStyleSheet('')

    return metal, verre

def detection():

    prev = 0
    current = 0

    while True:

        ok, res = cam.read()

        #cv2.imwrite("original.jpg", res)
        
        res = res[75:425,50:640]
        res = np.rot90(res)
        res = np.rot90(res)
        res = np.rot90(res)

        #cv2.imwrite("cropped.jpg", res)

        res = cv2.resize(res, (224,224))

        cv2.imwrite("resized.jpg", res)

        image_array = np.asarray(res)

        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        data[0] = normalized_image_array

        res = model.predict(data)

        #print(res)
        
        dlg.bar1.setValue(100 * res[0][0])
        dlg.bar2.setValue(100 * res[0][1])
        dlg.bar3.setValue(100 * res[0][2])
        dlg.bar4.setValue(100 * res[0][3])
        dlg.bar5.setValue(100 * res[0][4])
        dlg.bar6.setValue(100 * res[0][5])
        dlg.bar7.setValue(100 * res[0][6])
        dlg.bar8.setValue(100 * res[0][7])
        dlg.bar9.setValue(100 * res[0][8])
        dlg.bar10.setValue(100 * res[0][9])
        dlg.bar11.setValue(100 * res[0][10])
        dlg.bar12.setValue(100 * res[0][11])
        dlg.bar13.setValue(100 * res[0][12])
        dlg.bar14.setValue(100 * res[0][13])
        dlg.bar15.setValue(100 * res[0][14])

        current = np.argmax(res)


        metal, cap = setMetalCap()
        """
        if current == 0 and metal == False:
            if cap == False:
                dlg.pet1.setStyleSheet('QLabel#pet1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
                dlg.petfull1.setStyleSheet('')
            else:
                dlg.pet1.setStyleSheet('')
                dlg.petfull1.setStyleSheet('QLabel#petfull1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        elif metal == True:
            dlg.notsure1.setStyleSheet('QLabel#notsure {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.pet1.setStyleSheet('')
        
        ###############################################################""
        if current == 1 and metal == False:
            pass
        elif metal == True:
            dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.notsure1.setStyleSheet('')
        
        ##################################################################""
        if current == 2 and metal == False:
            if cap == False:
                dlg.carton1.setStyleSheet('QLabel#carton1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        elif metal == True:
            dlg.tetra1.setStyleSheet('QLabel#tetra1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.carton1.setStyleSheet('')
            dlg.tetra1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')
        ##################################################################""
        if current == 4 and metal == False:
            if cap == False:
                dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
            else:
                dlg.alu1.setStyleSheet('QLabel#alu1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        elif metal == True:
            dlg.acier1.setStyleSheet('QLabel#acier1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.acier1.setStyleSheet('')
            dlg.alu1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')
        
        ##################################################################""
        if current == 5:
            if metal == True and cap == True:
                dlg.acier1.setStyleSheet('QLabel#acier1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
            else:
                dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.acier1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')
        
        ##################################################################""
        if current == 6:
            if metal == False and cap == False:
                dlg.filme1.setStyleSheet('QLabel#filme1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
            else:
                dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.filme1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')
        ##################################################################""
        if current == 7:
            if metal == False and cap == False:
                dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
            elif cap == True:
                dlg.glass1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.glass1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')
        ##################################################################""
        if current == 14:
            if metal == True:
                dlg.notsure1.setStyleSheet('QLabel#notsure1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
            else:
                dlg.pehd1.setStyleSheet('QLabel#glass1 {border-style: outset;border-width: 2px;border-radius: 10px;border-color: green;}')
        else:
            dlg.pehd1.setStyleSheet('')
            dlg.notsure1.setStyleSheet('')

        """
    


        

#dlg.startButton.clicked.connect(detection)

if __name__ == "__main__":
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    



dlg.show()

Thread(target=detection).start()

sys.exit(app.exec_())
