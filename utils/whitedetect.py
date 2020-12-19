import cv2
import numpy as np
import random


def CheckWhite(img, x, y, far, radius, count, show=False):

    # If we are out of range return true
    if x+far < img.shape[1] and x + far > 0:
        b, g, r = img[y,x+far]
        if far > 0:
            trackX, trackY = x+radius+4, y+5
        else:
            trackX, trackY = x-radius-4, y+5
        if trackY > 99:
            trackY = 99
        try:
            b2, g2, r2 = img[trackY, trackX]
        except IndexError:
            b2, g2, r2 = 0, 0, 0
        #print(f"R2: {r2} G2: {g2} B2: {b2}")
    else:
        print("WHITE-OFF")
        return True

    if show:
        print(f"r: {r} g: {g} b: {b}")
        img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
        img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
        img = cv2.circle(img, (trackX, trackY), radius=2, color=(0, 255, 0), thickness=-1)
        cv2.imshow(f"ColorImage", img)
        cv2.waitKey(0)

    if(sum((r,g,b)) >= 760) and (sum((r2,g2,b2)) < 760):
        img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
        img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
        print(f"WHITE Wall - {count}")
        return True
    # elif(sum((r,g,b)) <= 320):
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Dark Wall- {count}")
    #     return True
    # Commenting out for black track
    # elif b > 80 and b <= 180 and g >= 75 and g <= 150 and r >= 80 and r <= 128:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print("Gray Wall")
    #     return True
    # Dark green Wall
    # elif b > 80 and b <= 90 and g >= 140 and g <= 150 and r >= 90 and r <= 100:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Green Wall - {count}")
    #     return True
    # Dark purple Wall CUT OUT FOR FALSE POSITVE
    # elif b >= 125 and b <= 215 and g >= 50 and g <= 110 and r >= 44 and r <= 182:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Purple Wall - {count}")
    #     return True
    # Dark RED Wall
    # elif b >= 40 and b <= 86 and g >= 40 and g <= 86 and r >= 115 and r <= 220:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Red Wall - {count}")
    #     return True
    # # Dark Yellow Wall
    # elif b > 57 and b <= 127 and g >= 120 and g <= 213 and r >= 48 and r <= 209:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Yellow Wall - {count}")
    #     return True
    # # Dark Blue starting Wall
    # elif b >= 112 and b <= 228 and g >= 82 and g <= 153 and r >= 50 and r <= 89:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Blue Wall - {count}")
    #     return True
    # # Dark Teal 
    # elif b >= 128 and b <= 220 and g >= 120 and g <= 225 and r >= 56 and r <= 88:
    #     img = cv2.circle(img, (x,y), radius=2, color=(0, 0, 0), thickness=-1)
    #     img = cv2.circle(img, (x+far,y), radius=2, color=(0, 0, 255), thickness=-1)
    #     print(f"Teal Wall - {count}")
    #     return True
    else:
        return False

def ShowCircles(color):
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    lines = cv2.Canny(color, threshold1=0, threshold2=398)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=20, minRadius=9, maxRadius=25)

    if circles is not None:
        circles = np.uint16(circles)
        print(len(circles))
        for pt in circles[0, :]:
            if pt[1] > 85 or pt[1] < 75:
                continue
            x, y, r = pt[0], pt[1], pt[2]
            print(r)
            cv2.circle(color, (x,y), r, (0, 0, 255), 5)

    cv2.imshow(f"Cirles", color)
    cv2.imshow(f"Lines", lines)
    cv2.waitKey(0)


if __name__ == "__main__":  
    img = cv2.imread("C:/Users/programmer/Desktop/LInes/ZigZag/images/" + '1148--CHECKWHITE-CLICKTrue-266-26-38-11.png', cv2.IMREAD_COLOR)
    answer = CheckWhite(img, 266, 26, -38, 11, 1, True)
    ShowCircles(img)
    print(answer)