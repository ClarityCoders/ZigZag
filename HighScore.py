import numpy as np
import cv2
import time
import mss
import pyautogui

from utils.getkeys import key_check
from utils.whitedetect import CheckWhite

# pyautogui has a built in delay set it to 0
pyautogui.PAUSE = 0
# Count down to get mouse in place
for i in range(1,5):
    print(i)
    time.sleep(1)

# Starts game
pyautogui.click()

# Create some setup variables
sct = mss.mss()
goingRight = True
count = 0
kernel = np.ones((3,3), np.uint8)

# Used to hold images until game is over then we can 
# write them to disk.
image_holder = []

# Start game loop
# holding h will break loop
while True:
    keys = key_check()
    if keys == "H":
        break

    count += 1

    # Define our area and grab screen.
    scr = sct.grab({
        'left': 0,
        'top': 390,
        'width': 440,
        'height': 50
    })

    # Turn screen grab into numpy array.
    img = np.array(scr)

    # Create a black array of same shape.
    # This will hold our edge lines later.
    black = np.zeros((50,440))

    # Create a color image and HSV to use for masking out
    # the diamonds.
    color = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    # Create a mask for diamonds. I got values by using the silders
    # in the lineDetection.py program.
    mask = cv2.inRange(hsv, np.array([153, 96, 175]), np.array([156, 255, 255]))

    # Gray image will be used to find circles
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Take our color images and find edges
    lines = cv2.Canny(color, threshold1=190, threshold2=135)

    # Diate our make so we know it will cover edges of diamonds.
    # Then mask out our line image.
    mask = cv2.dilate(mask, kernel, iterations=1)
    lines[mask>0]=0

    # Find Houghlines and paint them on our black image array.
    # I found these parameters by using sliders in the lineDetection.py program.
    HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = 19, minLineLength = 20, maxLineGap = 1)
    if HoughLines is not None:
        for line in HoughLines:
            coords = line[0]
            cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

    # Use HoughCircles to find the wall on the path.
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=18, minRadius=10, maxRadius=14)
    if circles is not None:
        circles = np.uint16(circles)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]

            # These values define how far to the right or left of the ball
            # we check to find a wall.
            pushFar = 38
            pushShort = 15
            lookUp = -3

            # Added some white detection in case the HoughLines fail
            if goingRight:
                answer = CheckWhite(color, x, y+lookUp, pushFar, r, count)
                if not answer:
                    answer = CheckWhite(color, x, y, pushFar, r, count)
            else:
                answer = CheckWhite(color, x, y+lookUp, -pushFar, r, count)
                if not answer:
                    answer = CheckWhite(color, x, y, -pushFar, r, count)

            # If we found a white wall click.
            if answer:
                goingRight = not goingRight
                pyautogui.click()
                time.sleep(0.02)
                image_holder.append((img, f"{count}--CHECKWHITE-CLICK{goingRight}-{x}-{y}-{pushFar}-{r}.png"))
                continue

            # if we find edge to right click with lookahead
            if sum(black[y+lookUp,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                pyautogui.click()
                time.sleep(0.02)
                goingRight = False
                image_holder.append((img, f"{count}color{x}-{y}-{r}_{x+r+pushShort}-{x+pushFar}_{y+lookUp}_HitRight.png"))

            # if we find edge to left click with lookahead
            elif not goingRight and sum(black[y+lookUp,x-pushFar : x-r-pushShort]) > 0:
                pyautogui.click()
                time.sleep(0.02)
                goingRight = True
                image_holder.append((img, f"{count}color{x}-{y}-{r}_{x-pushFar}-{x-r-pushShort}_{y+lookUp}_HitLeft.png"))

            # if we find edge to right click
            elif sum(black[y,x+r+pushShort:x+pushFar]) > 0 and goingRight:
                pyautogui.click()
                time.sleep(0.02)
                goingRight = False
                image_holder.append((img, f"{count}color{x}-{y}-{r}_{x+r+pushShort}-{x+pushFar}_{y+lookUp}_HitRightY2.png"))

            # if we find edge to left click
            elif not goingRight and sum(black[y,x-pushFar : x-r-pushShort]) > 0:
                pyautogui.click()
                time.sleep(0.02)
                goingRight = True
                image_holder.append((img, f"{count}color{x}-{y}-{r}_{x-pushFar}-{x-r-pushShort}_{y+lookUp}_HitLeftY2.png"))
            else:
                image_holder.append((img, f"{count}color_nohit-{x}-{y}-{r}.png"))

    # IF after the game has started we can't find ball note that!
    # Use the balls last position to make an educated guess.
    elif count > 50:
        if goingRight:
            x = x + 1
            answer = CheckWhite(color, x, y, pushFar, r, count)
            image_holder.append((img, f"{count}color_{x}_{y}_{pushFar}_{answer}GUESS.png"))
        else:
            x = x - 1
            answer = CheckWhite(color, x, y, -pushFar, r, count)
            image_holder.append((img, f"{count}color_{x}_{y}_{-pushFar}_{answer}GUESS.png"))

        if answer:
            goingRight = not goingRight
            pyautogui.click()
            time.sleep(0.02)
            continue

        print(f"{count} - No BALLS!")

# Do you want to write images?
response = input("Write images: y/n")

# Write images to disk.
if response.lower() == "y":
    for image in image_holder[-500:]:
        cv2.imwrite("images/"+ image[1], image[0])
