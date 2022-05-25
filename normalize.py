import numpy as np

def norm(points):
    points = np.array(points)

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    # centroid
    C = np.array([sum(x)/len(x), sum(y)/len(y), 1])

    dist = lambda x : np.dot(x-C, x-C)
    # mean distance to new origin
    mean = 2*sum([dist(p) for p in points])**0.5/len(points)

    s = 2**0.5/mean
    T = np.array([[s, 0, -s*C[0]], [0, s, -s*C[1]], [0,0,1]])

    # now C is the origin
    # avg dist to C is sqrt(2)
    print('oba', np.reshape(np.reshape(points[0], (3,1)),(1,3)).ravel())
    return T, [np.reshape(T@np.reshape(p, (3,1)), (1,3)).ravel() for p in points]

def intersections(l, w, h):
    a, b, c = l
    p = ()
    if -c/b > 0:
        p = (0, -int(c//b))
    
    
    if -(c + a*w)/b > 0:
        if p != ():
            q = (0, -int((c + a*w)/b))
            print(p, q, 'oua1')
            return p, q
        print( b, ' ', c)
        p = (0, -int((c + a*w)/b))
    
    if -c/a > 0:
        if p != ():
            q = (-int(c/a), 0)
            return p,q
            print(p, q, 'oua2')
        p = (-int(c/a), 0)

    q = (-int((c+b*h)/a), 0)
    print(p, q, 'oua3')
    return p, q
    