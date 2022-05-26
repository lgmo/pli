import cv2
import csv
from utils import *
from os.path import exists

def equationmatrix(x1,x2):
    npts = x1.shape[1]
    A = c_[x2[0]*x1[0], x2[0]*x1[1], x2[0], x2[1]*x1[0], x2[1]*x1[1], x2[1], x1[0], x1[1], ones((npts,1))]
    return A

img1 = cv2.imread(IMG1_PATH)
img2 = cv2.imread(IMG2_PATH)

img1 = cv2.resize(img1, (HEIGHT, WIDTH))
img2 = cv2.resize(img2, (HEIGHT, WIDTH))

pointsimg1, pointsimg2 = getpoints()

T , pointsimg1l = norm(pointsimg1)
Tl, pointsimg2l = norm(pointsimg2)


A = equationmatrix(array(pointsimg1l).T, array(pointsimg2l).T)
_, _, V = linalg.svd(A)

print(V, 'slah')
V = V.T

Fl = V[:,8].reshape(3,3).copy()
U, D, V = linalg.svd(Fl)

Fl = U @ diag([D[0], D[1], 0]) @ V

F = Tl.T @ Fl @ T
print('mf', F)

for p in pointsimg1:
        cv2.circle(img1, (p[0],p[1]), 3, (255, 50,50),-1)

for p in pointsimg2:
    cv2.circle(img2, (p[0],p[1]), 3, (50,255, 50),-1)

x = 0
for p in pointsimg1:
    p = reshape(transpose(array(p)),(3,1))
    cv2.circle(img1, (int(p[0]), int(p[1])), 3,(255,50, 255),-1)
    cv2.waitKey(0)
    l = reshape(F @ p, (1,3)).ravel()
    if l[0] == 0:
        print()
        cv2.line(img2, (0,-int(l[2]/l[1])), (widht//4,-l[2]/l[1]), (50,50,255), thickness=2)
    elif l[1] == 0:
        print()
        cv2.line(img2, (-int(l[2]/l[0]), 0), (-int(l[2]/l[0]), width//4), (50, 50, 255), thickness=2)
    else:
        p1, p2 = intersections(l, WIDTH, HEIGHT)
        print(p1, 'iou', p2)
        cv2.line(img2, p1, p2, (50,50,255), thickness=2)
    cv2.imshow('image2',img2)
    cv2.imshow('image1', img1)
cv2.waitKey(0)