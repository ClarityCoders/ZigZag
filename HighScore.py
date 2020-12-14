from ppadb.client import Client
import numpy as np
import cv2
import time
import mss
import pyautogui

from utils.getkeys import key_check

pyautogui.PAUSE = 0
for i in range(1,5):
    print(i)
    time.sleep(1)

pyautogui.click()

start_t = time.time()



sct = mss.mss()
goingRight = True
count = 0
kernel = np.ones((2,2), np.uint8)

image_holder = []

while True:

    keys = key_check()
    if keys == "H":
        break

    count += 1
    scr = sct.grab({
        'left': 0,
        'top': 385,
        'width': 440,
        'height': 50
    })
    img = np.array(scr)
    black = np.zeros((50,440))

    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    #Mask
    mask = cv2.inRange(hsv, np.array([151, 96, 175]), np.array([154, 255, 255]))
    color[mask>0]=(255,255,152)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lines = cv2.Canny(color, threshold1=100, threshold2=120)
    img_dilation = cv2.dilate(lines, kernel, iterations=1) 

    #HoughLines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, 37, 3, 22)
    HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = 31, minLineLength = 20, maxLineGap = 1)
    if HoughLines is not None:
        for line in HoughLines:
            coords = line[0]
            cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=17, minRadius=10, maxRadius=14)
    if circles is not None:
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            #cv2.circle(img, (x,y), r, (0, 0, 255), 5)

            pushFar = 38
            pushShort = 10
            lookUp = -3

            if x+pushFar <= 400:
                rightColor = int(black[y+lookUp,x+pushFar])
            else:
                rightColor = 400
            leftColor = int(black[y+lookUp,x-pushFar])

            if x+r+pushShort <= 400:
                rightBallColor = int(black[y+lookUp,x+r+pushShort])
            else:
                rightBallColor = 400

            if x-r-pushShort >= 0:
                leftBallColor = int(black[y+lookUp,x-r-pushShort])
            else:
                leftBallColor = 0

            # Switch to left.
            diff = abs(rightColor - rightBallColor)

            # Switch to right test
            diff2 = abs(leftColor - leftBallColor)

            if sum(black[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                pyautogui.click()
                goingRight = False
                image_holder.append((img, f"{count}color_{x+r+pushShort}-{x+pushFar}_{y+lookUp}_HitRight.png"))

            elif not goingRight and sum(black[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                pyautogui.click()
                goingRight = True
                image_holder.append((img, f"{count}color_{x-pushFar}-{x-r-pushShort}_{y+lookUp}_HitLeft.png"))
            else:
                image_holder.append((img, f"{count}color_nohit.png"))
    else:
        image_holder.append((img, f"{count}color_noBALL-------------------.png"))
        print(f"{count} - No BALLS!")

    end_t = time.time()
    time_taken = end_t - start_t
    start_t = end_t

# Do you want to write images?
response = input("Write images: y/n")

if response.lower() == "y":
    for image in image_holder:
        cv2.imwrite("images/"+ image[1], image[0])
