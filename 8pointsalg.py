import cv2
import numpy as np

points = []
curwindow = 1
def drawpoint(event, x, y, flags, param):
    global curwindow
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if curwindow == 1:
            cv2.circle(img1, (x,y), 3, (255,50, 50),-1)
            curwindow += 1
        else:
            cv2.circle(img2, (x,y), 3, (255,50, 50),-1)
            curwindow -= 1
        points.append([x,y,1])


img1 = cv2.imread('img1.JPG')
height, width, _ = img1.shape
img1 = cv2.resize(img1, (width//4, height//4))
img2 = cv2.imread('img2.JPG')
height, widht, _ = img2.shape
img2 = cv2.resize(img2, (width//4, height//4))

cv2.namedWindow('image1')
cv2.namedWindow('image 2')
cv2.setMouseCallback('image1', drawpoint)
cv2.setMouseCallback('image 2', drawpoint)

while 1:
    cv2.imshow('image1', img1)
    cv2.imshow('image 2', img2)
    k = cv2.waitKey(20) & 0xFF
    if len(points) == 16:
        break

A = np.array([])
for i in range(8):
    p = points[i]
    q = points[8+i]
    A += np.kron(q,p)

