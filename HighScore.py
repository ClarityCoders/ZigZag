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
kernel = np.ones((3,3), np.uint8)

image_holder = []

while True:

    keys = key_check()
    if keys == "H":
        break

    count += 1
    scr = sct.grab({
        'left': 0,
        'top': 390,
        'width': 440,
        'height': 50
    })
    img = np.array(scr)
    black = np.zeros((50,440))

    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    #Mask
    mask = cv2.inRange(hsv, np.array([153, 96, 175]), np.array([156, 255, 255]))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lines = cv2.Canny(color, threshold1=190, threshold2=135)
    mask = cv2.dilate(mask, kernel, iterations=1)
    lines[mask>0]=0

    HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = 19, minLineLength = 19, maxLineGap = 1)
    if HoughLines is not None:
        for line in HoughLines:
            coords = line[0]
            cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=18, minRadius=10, maxRadius=14)
    if circles is not None:
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]

            pushFar = 38
            pushShort = 8
            lookUp = -3
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
