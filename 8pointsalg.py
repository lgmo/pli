import cv2
import csv
import numpy as np
from os.path import exists

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
cv2.namedWindow('image2')
if not exists('points.csv'):
    cv2.setMouseCallback('image1', drawpoint)
    cv2.setMouseCallback('image2', drawpoint)
else:
    with open('points.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            line = [int(i) for i in row]
            points.append(line)

while 1:
    cv2.imshow('image1', img1)
    cv2.imshow('image2', img2)
    k = cv2.waitKey(20) & 0xFF
    if len(points) == 16 or exists('points.csv'):
        break

with open('points.csv', 'w') as f:
    writer = csv.writer(f)
    for p in points:
        writer.writerow(p)

A = []
for i in range(8):
    p = np.array(points[i])
    q = np.array(points[8+i])
    print(p)
    print(q)
    print(np.kron(q,p))
    A.append(np.kron(q,p))

A = np.array(A)


_, _, V = np.linalg.svd(A)

Fl = np.reshape(V[8], (3,3))

U, S, V = np.linalg.svd(Fl)

print(S)

F = U * np.diag([S[1], S[2], 0]) * np.transpose(V)


for p in points[:len(points)//2]:
    p = np.reshape(np.transpose(np.array(p)),(3,1))
    l = F@p
    print(p)
    print(l)
    if l[0][0] == 0:
        cv2.line(img2, (0,int(l[2][0]/l[1][0])), (widht//4,l[2][0]/l[1][0]), (255,0,0), thickness=2)
    elif l[1][0] == 0:
        cv2.line(img2, (int(l[2][0]/l[0][0]), 0), (int(l[2][0]/l[0][0]), height//4), (255, 0, 0), thickness=2)
    else:
        print(l[2][0]/l[0][0], " slah ", l[2][0]/l[1][0])
        cv2.line(img2, (int(l[2][0]/l[0][0]), 0), (0,int(l[2][0]/l[1][0])), (255,0,0), thickness=3)
    cv2.imshow('image2',img2)
cv2.waitKey(0)