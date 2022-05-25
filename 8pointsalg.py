import cv2
import csv
from normalize import *
from os.path import exists

NCORR = 8

img1 = cv2.imread('img1.JPG')
img2 = cv2.imread('img2.JPG')

width, height, _ = img1.shape

img1 = cv2.resize(img1, (height//4, width//4))
img2 = cv2.resize(img2, (height//4, width//4))

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



T, pointsimg1l = norm(pointsimg1)
Tl, pointsimg2l =  norm(pointsimg2)

A = []
for i in range(NCORR):
    p = np.array(pointsimg1l[i])
    q = np.array(pointsimg2l[i])
    A.append(np.kron(q,p))

_, _, V = np.linalg.svd(A)

Fl = np.reshape(V[8], (3,3))

F = np.transpose(Tl)@Fl@T
for p in pointsimg1:
    cv2.circle(img1, (p[0],p[1]), 3, (255, 50,50),-1)

for p in pointsimg2:
    cv2.circle(img2, (p[0],p[1]), 3, (50,255, 50),-1)

for p in pointsimg1:
    p = np.reshape(np.transpose(np.array(p)),(3,1))
    cv2.waitKey(0)
    l = np.reshape(F@p, (1,3)).ravel()
    print(l)
    print(p)
    print(l)
    if l[0] == 0:
        cv2.line(img2, (0,-int(l[2]/l[1])), (widht//4,-l[2]/l[1]), (50,50,255), thickness=2)
    elif l[1] == 0:
        cv2.line(img2, (-int(l[2]/l[0]), 0), (-int(l[2]/l[0]), height//4), (50, 50, 255), thickness=2)
    else:
        p, q = intersections(l, width//4, height//4)
        if p == ():
            continue
        cv2.line(img2, p, q, (50,50,255), thickness=2)
    cv2.imshow('image2',img2)
    cv2.imshow('image1', img1)
cv2.waitKey(0)

# while 1:
#     points = []
#     curwindow = 0
#     def drawpoint(event, x, y, flags, param):
#         global curwindow
#         if event == cv2.EVENT_LBUTTONDBLCLK:
#             if curwindow < 8:
#                 cv2.circle(img1, (x,y), 3, (255,50, 50),-1)
#                 curwindow += 1
#             else:
#                 cv2.circle(img2, (x,y), 3, (255,50, 50),-1)
#             points.append([x,y,1])

#     img1 = cv2.imread('img1.JPG')
#     height, width, _ = img1.shape
#     img1 = cv2.resize(img1, (width//4, height//4))
#     img2 = cv2.imread('img2.JPG')
#     height, widht, _ = img2.shape
#     img2 = cv2.resize(img2, (width//4, height//4))

#     cv2.namedWindow('image1')
#     cv2.namedWindow('image2')
#     if not exists('points.csv'):
#         cv2.setMouseCallback('image1', drawpoint)
#         cv2.setMouseCallback('image2', drawpoint)
#     else:
#         with open('points.csv') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 line = [int(i) for i in row]
#                 points.append(line)

#     while 1:
#         cv2.imshow('image1', img1)
#         cv2.imshow('image2', img2)
#         k = cv2.waitKey(20) & 0xFF
#         if len(points) == 16 or exists('points.csv'):
#             break

#     if not exists('points.csv'):
#         with open('points.csv', 'w') as f:
#             writer = csv.writer(f)
#             for p in points:
#                 writer.writerow(p)

#     for [x,y,_] in points[:len(points)//2]:
#         cv2.circle(img1, (x,y), 3, (255,50, 50),-1)

#     for [x,y,_] in points[len(points)//2:]:
#         cv2.circle(img2, (x,y), 3, (50,255, 50),-1)

#     cv2.imshow('image1', img1)
#     cv2.imshow('image2', img2)

#     T, pointsl = norm(points[:len(points)//2])
#     Tl, aux = norm(points[len(points)//2:])
#     pointsl += aux

#     pointsl = np.array(pointsl)
#     A = []
#     for i in range(8):
#         p = np.array(pointsl[i])
#         q = np.array(pointsl[8+i])
#         print(p)
#         print(q)
#         print(np.kron(q,p))
#         A.append(np.kron(q,p))

#     A = np.array(A)


#     _, _, V = np.linalg.svd(A)

#     Fl = np.reshape(V[8], (3,3))

#     F = np.linalg.inv(Tl)@Fl@T 
#     print('oba', F)
#     for p in points[:len(points)//2]:
#         cv2.circle(img1, (p[0],p[1]), 3, (50,50, 255),-1)
#         p = np.reshape(np.transpose(np.array(p)),(3,1))
#         cv2.waitKey(0)
#         l = np.reshape(F@p, (1,3)).ravel()
#         print(p)
#         print(l)
#         if l[0] == 0:
#             cv2.line(img2, (0,-int(l[2]/l[1])), (widht//4,-l[2]/l[1]), (50,50,255), thickness=2)
#         elif l[1] == 0:
#             cv2.line(img2, (-int(l[2]/l[0]), 0), (-int(l[2]/l[0]), height//4), (50, 50, 255), thickness=2)
#         else:
#             p, q = intersections(l, width//4, height//4)
#             if p == ():
#                 continue
#             cv2.line(img2, p, q, (50,50,255), thickness=2)
#         cv2.imshow('image2',img2)
#         cv2.imshow('image1', img1)
    # cv2.waitKey(0)