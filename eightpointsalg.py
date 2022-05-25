import cv2
import csv
from utils import *
from os.path import exists

NCORR = 8

img1 = cv2.imread('img1.JPG')
img2 = cv2.imread('img2.JPG')

height, width, _ = img1.shape

img1 = cv2.resize(img1, (width//4, height//4))
img2 = cv2.resize(img2, (width//4, height//4))

pointsimg1 = []
pointsimg2 = []
count = 0

with open('points.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        line = [int(i) for i in row]
        if count % 2:
            pointsimg2.append(line)
        else:
            pointsimg1.append(line)
        count += 1
    
def equationmatrix(x1,x2):
    npts = x1.shape[1]
    A = c_[x2[0]*x1[0], x2[0]*x1[1], x2[0], x2[1]*x1[0], x2[1]*x1[1], x2[1], x1[0], x1[1], ones((npts,1))]
    return A

T , pointsimg1l = norm(pointsimg1)
Tl, pointsimg2l = norm(pointsimg2)


A = equationmatrix(array(pointsimg1l).T, array(pointsimg2l).T)
_, _, V = linalg.svd(A)

V = V.conj().T

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
# cv2.line(img2, (213+x,312), (262+x,0), (50,50,255), thickness=2)
for p in pointsimg1:
    p = reshape(transpose(array(p)),(3,1))
    cv2.circle(img1, (int(p[0]), int(p[1])), 3,(255,50, 255),-1)
    cv2.waitKey(0)
    l = reshape(F@p, (1,3)).ravel()
    l = l*1000
    print(f'{l[0]:.6f}, {l[1]:.6f}, {l[2]:.6f}')
    # print(p)
    if l[0] == 0:
        print()
        cv2.line(img2, (0,-int(l[2]/l[1])), (widht//4,-l[2]/l[1]), (50,50,255), thickness=2)
    elif l[1] == 0:
        print()
        cv2.line(img2, (-int(l[2]/l[0]), 0), (-int(l[2]/l[0]), width//4), (50, 50, 255), thickness=2)
    else:
        p1, p2 = intersections(l, width//4, height//4)
        
        print(p1, 'iou', p2)
        cv2.line(img2, p1, p2, (50,50,255), thickness=2)
    cv2.imshow('image2',img2)
    cv2.imshow('image1', img1)
cv2.waitKey(0)