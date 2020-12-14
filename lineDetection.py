import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 151, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 96, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 175, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 154, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Thresh1", "Trackbars", 100, 400, nothing)
cv2.createTrackbar("Thresh2", "Trackbars", 120, 400, nothing)

cv2.createTrackbar("hThresh", "Trackbars", 31, 400, nothing)
cv2.createTrackbar("hMinLine", "Trackbars", 20, 100, nothing)
cv2.createTrackbar("hMaxGap", "Trackbars", 1, 100, nothing)

kernel = np.ones((2,2), np.uint8) 
while True:

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    Thresh1 = cv2.getTrackbarPos("Thresh1", "Trackbars")
    Thresh2 = cv2.getTrackbarPos("Thresh2", "Trackbars")
    hThresh = cv2.getTrackbarPos("hThresh", "Trackbars")
    hMinLine = cv2.getTrackbarPos("hMinLine", "Trackbars")
    hMaxGap = cv2.getTrackbarPos("hMaxGap", "Trackbars")

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    images = [
        cv2.imread('exampleWhite-NoLines.png', cv2.IMREAD_COLOR),
        cv2.imread('example-left-hit.png', cv2.IMREAD_COLOR),
        cv2.imread('example-hit-left2.png', cv2.IMREAD_COLOR),
        #cv2.imread('color-Fixed-4.png', cv2.IMREAD_COLOR),
        #cv2.imread('color-Fixed-3.png', cv2.IMREAD_COLOR),
        #cv2.imread('color-Fixed-2.png', cv2.IMREAD_COLOR),
        #cv2.imread('color-Fixed-1.png', cv2.IMREAD_COLOR)
    ]
    black = np.zeros((50,440))

    for i, img in enumerate(images):
        black = np.zeros((50,440))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #mask = 255 - mask
        # No Mask
        result = img

        #use mask
        #result = cv2.bitwise_and(img, img, mask=mask)
        result[mask>0]=(255,255,152)

        lines = cv2.Canny(result, threshold1=Thresh1, threshold2=Thresh2)
        img_dilation = cv2.dilate(lines, kernel, iterations=1) 

        #HoughLines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, hThresh, hMinLine, hMaxGap
        HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = hThresh, minLineLength = hMinLine, maxLineGap = hMaxGap)
        if HoughLines is not None:
            for line in HoughLines:
                coords = line[0]
                cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [0,0,255], 3)
                cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

        #cv2.imshow(f"Mask{i}", mask)
        cv2.imshow(f"Original{i}", img)
        #cv2.imshow(f"Result{i}", result)
        cv2.imshow(f"Lines{i}", lines)
        #cv2.imshow(f"Dilation{i}", img_dilation)
        #cv2.imshow(f"blacknWhite{i}", black)
        cv2.waitKey(1)
