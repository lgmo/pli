from numpy import *

def norm(points):
    points = array(points)

    x = [p[0] for p in points]
    y = [p[1] for p in points]
    print(x,'hmmm')
    # centroid
    print('boba', sum(x)/len(x))
    C = array([mean(array(x)), mean(array(y)), 1])

    dist = lambda x : dot(x-C, x-C)**0.5
    # mean distance to new origin
    mn = mean(array([dist(p) for p in points]))

    s = 2**0.5/mn
    T = array([[s, 0, -s*C[0]], [0, s, -s*C[1]], [0,0,1]])

    # now C is the origin
    # avg dist to C is sqrt(2)
    print('oba', reshape(reshape(points[0], (3,1)),(1,3)).ravel())
    return T, [reshape(T@reshape(p, (3,1)), (1,3)).ravel() for p in points]

def intersections(l, w, h):
    point = lambda p: (int(p[0]/p[2]), int(p[1]/p[2]))
    p1 = cross(l, array([1,0,0]))
    p1 = point(p1)
    
    p2 = cross(l, array([0,1,0]))
    p2 = point(p2)
    print(p2)
    p3 = cross(l, array([1,0,w]))
    p3 = point(p3)
    p4 = cross(l, array([0,1,-h]))
    print(array([0,1,h]))
    print('b', l)
    print('a', p4)
    p4 = point(p4)

    a = [p1, p2, p3, p4]
    entre = lambda x, y, z: y <= x and x <= z
    print(a)
    p = (-1,-1)
    for x in a:
        if entre(x[0], 0, w) and entre(x[1], 0, h):
            p = x
            break
    q = (-1,-1)
    for x in a:
        if entre(x[0], 0, w) and entre(x[1], 0, h) and x != p:
            q = x
            break
    return p, q
    