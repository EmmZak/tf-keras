import tensorflow.keras
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from time import time
import numpy as np
import cv2
from time import time, sleep
import os
from threading import Thread
import plc
cam = cv2.VideoCapture(0)
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
#####################################################################################" model "
model = tensorflow.keras.models.load_model('converted_keras/keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
classes = open("converted_keras/labels.txt").readlines()
#####################################################################################" model "
global permission
permission = True

global res1
global res2
global res3
global res4
global res5
res1 = None
res2 = None
res3 = None
res4 = None
res5 = None

def permissionPrint():
    global permission
    while True:
        print("-----" + str(permission) + "-----")

def play(n):
    global permission
    permission = False

    os.system("play voice/" + str(n) + ".wav -q")

    if n == 3:
        plc.setCoil(1)
        permission = True
        return

    if n == 4:
        plc.setCoil(2)
        permission = True
        return

    if n == 7:
        plc.setCoil(3)
        permission = True
        return

    if n == 1:
        plc.setCoil(7)
        permission = True
        return

    if n == 5:
        plc.setCoil(6)
        permission = True
        return

    if n == 6:
        permission = True
        return
    
    sleep(2)    

    permission = True

def detect():

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

    return classes[np.argmax(res)]

def main():
    global permission
    global res1
    global res2
    global res3
    global res4

    res4 = detect()

    # while (res1 == res2 == res3 == res4) == False: 

    #     res1 = res2
    #     res2 = res3
    #     res3 = res4
    #     res4 = detect()

    #     try:
    #         print(classes[res1], classes[res2], classes[res3], classes[res4])
    #     except:
    #         print("Nothing")

    #print("permission -- {}".format(permission)) 

    if permission == False:
        return

    print(res4)

    if "12" in res4:
        Thread(target=play, args=(12,)).start()
    

def tf1():
    global permission

    res1 = None
    res2 = None
    res3 = None
    res4 = None
    res5 = None 
    res1 = detect()
    res2 = detect()
    res3 = detect()
    res4 = detect() 
    #res5 = detect() 

    #print("g{} {} {} {}".format(classes[res1], classes[res2], classes[res3], classes[res4]))#, classes[res5]))
    
    if permission == False:
        return

    if (res1 == res2 == res3 == res4): #== res5
        
        
        if res1 != 0:
            #play(res4)
            Thread(target=play, args=(res4,)).start()

        return res1

#Thread(target=permissionPrint).start()

while True:

    main()


