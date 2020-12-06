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
kernel = np.ones((2,2), np.uint8)
while True:
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

    lines = cv2.Canny(color, threshold1=271, threshold2=398)
    img_dilation = cv2.dilate(lines, kernel, iterations=1) 

    HoughLines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, 37, 3, 24)
    if HoughLines is not None:
        for line in HoughLines:
            coords = line[0]
            cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=40)
    if circles is not None:
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(img, (x,y), r, (0, 0, 255), 5)

            pushFar = 30
            pushShort = 6
            lookUp = -5

            if x+pushFar <= 400:
                rightColor = int(black[y+lookUp,x+pushFar])
            else:
                rightColor = 400
            leftColor = int(black[y+lookUp,x-pushFar])

            if x+r+pushShort <= 400:
                rightBallColor = int(black[y+lookUp,x+r+pushShort])
            else:
                rightBallColor = 400
            leftBallColor = int(black[y+lookUp,x-r-pushShort])

            # Switch to left.
            diff = abs(rightColor - rightBallColor)

            # Switch to right test
            diff2 = abs(leftColor - leftBallColor)

            if sum(black[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                pyautogui.click()
                goingRight = False
                #print("first")
                #cv2.imwrite(f"zleft{count}.png", black)
                cv2.imwrite(f"zleft-color{count}.png", color)

            elif not goingRight and sum(black[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                pyautogui.click()
                goingRight = True
                #cv2.imwrite(f"zright{count}.png", black)
                cv2.imwrite(f"zright-color{count}.png", color)

    #if count % 3 == 0:
        #cv2.imwrite(f"a{count}.png", color)
    end_t = time.time()
    time_taken = end_t - start_t
    start_t = end_t
