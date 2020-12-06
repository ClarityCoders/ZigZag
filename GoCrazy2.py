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
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(img, (x,y), r, (0, 0, 255), 5)

            pushFar = 30
            pushShort = 6
            lookUp = -5

            rightColor = int(lines[y+lookUp,x+pushFar])
            leftColor = int(lines[y+lookUp,x-pushFar])

            rightBallColor = int(lines[y+lookUp,x+r+pushShort])
            leftBallColor = int(lines[y+lookUp,x-r-pushShort])

            # Switch to left.
            diff = abs(rightColor - rightBallColor)

            # Switch to right test
            diff2 = abs(leftColor - leftBallColor)
            #print(leftColor, leftBallColor, rightBallColor, rightColor, diff, x+r+2, x+20, x-r-2, x-20)
            #print(diff)
            #print(leftColor, leftBallColor, rightBallColor, rightColor, diff)
            # if diff > 35 and goingRight:
            #print(y-10, x-r-pushShort, x-pushFar, goingRight)

            rightCrazy = lines[y,x+r]
            leftCrazy = lines[y,x-r]
            bottomCrazy = sum(lines[y+r,x-r:x+r])
            topCrazy = lines[y-r,x]
            print(rightCrazy, leftCrazy, bottomCrazy, topCrazy)

            if sum(lines[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                #print(y+lookUp, x-r-pushShort, x-pushFar)
                #print(sum(lines[y-10,x+pushShort:x+pushFar]))
                #print(x,y,r)
                #device.shell('input tap 500 500')
                pyautogui.click()
                #print("go left")
                #print(leftColor, leftBallColor, rightBallColor, rightColor, diff)
                goingRight = False
                gray = cv2.circle(gray, (x+pushFar,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x+r+pushShort,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x-pushFar,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                gray = cv2.circle(gray, (x-r-pushShort,y+lookUp), radius=1, color=(0, 255, 0), thickness=-1)
                cv2.imwrite(f"lines{count}.png", lines)
                cv2.imwrite(f"color{count}.png", color)
                #cv2.imwrite("Goleft.png", lines)
                #cv2.imwrite("GoleftColor.png", gray)
            #elif diff2 > 35 and not goingRight:
            elif not goingRight and sum(lines[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                #print(lines.shape)
                pyautogui.click()
                print("go right")
                #print(leftColor, leftBallColor, rightBallColor, rightColor, diff2)
                goingRight = True
                cv2.imwrite(f"lines{count}.png", lines)
                cv2.imwrite(f"color{count}.png", color)

    #cv2.imwrite(f"Goleft{count}.png", lines)
    #cv2.imwrite(f"GoleftColor.png", gray)

    cv2.imshow('Bot View', lines)
    cv2.waitKey(1)
    end_t = time.time()
    time_taken = end_t - start_t
    start_t = end_t