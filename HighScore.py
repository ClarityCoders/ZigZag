from ppadb.client import Client
import numpy as np
import cv2
import time
import mss
import pyautogui

pyautogui.PAUSE = 0
for i in range(1,5):
    print(i)
    time.sleep(1)

pyautogui.click()

start_t = time.time()

adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices) == 0:
    print("No devices found")

device = devices[0]

sct = mss.mss()
goingRight = True
count = 0
while True:
    count += 1
    scr = sct.grab({
        'left': 0,
        'top': 385,
        'width': 440,
        'height': 50
    })
    img = np.array(scr)
    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lines = cv2.Canny(img, threshold1=119, threshold2=250)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=40)
    if circles is not None:
        #print(len(circles))
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(img, (x,y), r, (0, 0, 255), 5)

            pushFar = 30
            pushShort = 6
            lookUp = -5

            if x+pushFar <= 400:
                rightColor = int(lines[y+lookUp,x+pushFar])
            else:
                rightColor = 400
            leftColor = int(lines[y+lookUp,x-pushFar])

            rightBallColor = int(lines[y+lookUp,x+r+pushShort])
            leftBallColor = int(lines[y+lookUp,x-r-pushShort])

            # Switch to left.
            diff = abs(rightColor - rightBallColor)

            # Switch to right test
            diff2 = abs(leftColor - leftBallColor)

            if sum(lines[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                pyautogui.click()
                goingRight = False
                gray = cv2.circle(gray, (x+pushFar,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x+r+pushShort,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x-pushFar,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x-r-pushShort,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)

            elif not goingRight and sum(lines[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                pyautogui.click()
                goingRight = True

    #cv2.imshow('Bot View', lines)
    #cv2.waitKey(1)
    end_t = time.time()
    time_taken = end_t - start_t
    start_t = end_t
