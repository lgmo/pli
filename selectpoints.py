import cv2
import csv

NCORR = 8

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
            curwindow = 1
        points.append([x,y,1])

img1 = cv2.imread('img1.JPG')
img2 = cv2.imread('img2.JPG')

width, height, _ = img1.shape

img1 = cv2.resize(img1, (height//4, width//4))
img2 = cv2.resize(img2, (height//4, width//4))

cv2.namedWindow('image1')
cv2.namedWindow('image2')

cv2.setMouseCallback('image1', drawpoint)
cv2.setMouseCallback('image2', drawpoint)

while 1:
    cv2.imshow('image1', img1)
    cv2.imshow('image2', img2)
    k = cv2.waitKey(20) & 0xFF
    if len(points) == 2*NCORR:
        break

with open('points.csv', 'w') as f:
    writer = csv.writer(f)
    for p in points:
        writer.writerow(p)