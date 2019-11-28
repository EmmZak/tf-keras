import cv2
from time import time
import numpy as np
from datetime import datetime
import os

cam = cv2.VideoCapture(0)
target = "cup"
count = 0

ok, img = cam.read()

crop = img[75:425,50:640]
crop = np.rot90(crop)
crop = np.rot90(crop)
crop = np.rot90(crop)

crop = cv2.resize(crop, (224,224))

cv2.imshow("crop", crop)
# cv2.imshow("img", img)

if os.path.isdir("training_images/" + target) == False:
    os.mkdir("training_images/" + target)

for count in range(50):
    cv2.imwrite("training_images/" + target + "/" + str(datetime.now()) + str(count) + ".jpg", crop)

    count += 1
    print(count)

    cv2.waitKey(1)

"""
while count < 100:

    ok, img = cam.read()

    crop = img[75:425,50:640]
    crop = np.rot90(crop)
    crop = np.rot90(crop)
    crop = np.rot90(crop)
    
    #cv2.rectangle(img, (50, 75), (640, 425), (0, 20, 200), 2)

    # img = np.rot90(img)
    # img = np.rot90(img)
    # img = np.rot90(img)

    cv2.imshow("crop", crop)
    # cv2.imshow("img", img)

    if os.path.isdir("training_images/" + target) == False:
        os.mkdir("training_images/" + target)

    cv2.imwrite("training_images/" + target + "/" + str(datetime.now()) + str(count) + ".jpg", crop)

    count += 1
    print(count)

    cv2.waitKey(1)
"""