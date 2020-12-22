from ppadb.client import Client
import numpy as np
import cv2
import time
import mss
import pyautogui
import random

from utils.getkeys import key_check
from utils.whitedetect import CheckWhite

episode_count = 0
total_Episodes = 1000
highscore = 0

while True and episode_count < total_Episodes:
    episode_count += 1
    keys = key_check()
    if keys == "H":
        break

    pyautogui.PAUSE = 0
    for i in range(1,5):
        #print(i)
        time.sleep(1)

    pyautogui.click()
    time.sleep(2)
    pyautogui.click()

    sct = mss.mss()
    goingRight = True
    
    count = 0
    kill_count = 0

    kernel = np.ones((3,3), np.uint8)

    # lookUp = random.randint(-3,3)
    # threshold = random.randint(10,50)
    # minLineLength = random.randint(10, 25)
    # maxLineGap = 1
    # pushFar = random.randint(35,40)
    # pushShort = random.randint(5, 20)

    lookUp = -4
    threshold = 19
    minLineLength = 19
    maxLineGap = 1
    pushFar = 38
    pushShort = 15

    while True:

        count += .085
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
        mask = cv2.inRange(hsv, np.array([153, 96, 175]), np.array([156, 255, 255]))
        #color[mask>0]=(255,255,152)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        lines = cv2.Canny(color, threshold1=190, threshold2=135)
        mask = cv2.dilate(mask, kernel, iterations=1)
        lines[mask>0]=0

        HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)
        if HoughLines is not None:
            for line in HoughLines:
                coords = line[0]
                cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=18, minRadius=10, maxRadius=14)
        if circles is not None:
            kill_count = 0
            circles = np.uint16(circles)
            for pt in circles[0, :]:
                x, y, r = pt[0], pt[1], pt[2]

                if y < 20 or y > 40:
                    continue

                if goingRight:
                    answer = CheckWhite(color, x, y+lookUp, pushFar, r, count)
                    if not answer:
                        answer = CheckWhite(color, x, y, pushFar, r, count)
                else:
                    answer = CheckWhite(color, x, y+lookUp, -pushFar, r, count)
                    if not answer:
                        answer = CheckWhite(color, x, y, -pushFar, r, count)

                if answer:
                    goingRight = not goingRight
                    pyautogui.click()
                    time.sleep(0.02)
                    continue

                if sum(black[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                    pyautogui.click()
                    time.sleep(0.02)
                    goingRight = False

                elif not goingRight and sum(black[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                    pyautogui.click()
                    time.sleep(0.02)
                    goingRight = True

                elif sum(black[y,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                    pyautogui.click()
                    time.sleep(0.02)
                    goingRight = False

                elif not goingRight and sum(black[y,x-pushFar : x-r-pushShort]) > 0:
                    pyautogui.click()
                    time.sleep(0.02)
                    goingRight = True
        elif count > 10:
            kill_count += 1
            if kill_count == 50:
                break
            if goingRight:
                x = x + 1
                answer = CheckWhite(color, x, y, pushFar, r, count)
            else:
                x = x - 1
                answer = CheckWhite(color, x, y, -pushFar, r, count)

            if answer:
                goingRight = not goingRight
                pyautogui.click()
                time.sleep(0.02)
                continue
    
    count = int(count)
    if highscore < count:
        highscore = count

    f = open("Stats.csv","a+")
    f.write(f"{episode_count},{count},{lookUp},{threshold},{minLineLength},{maxLineGap},{pushFar},{pushShort}\n")
    f.close()
    print(f"Episode: {episode_count} score: {count} highscore: {highscore} lookahead: {lookUp} Thresh: {threshold} min line: {minLineLength} Max Gap:{maxLineGap} PushFar: {pushFar} Push Short: {pushShort}")
