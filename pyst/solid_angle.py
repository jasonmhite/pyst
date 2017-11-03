import numpy as np

__all__ = ["RectangularFacet"]

## Fast triple product from https://stackoverflow.com/questions/42158228/fast-scalar-triple-product-in-numpy
# Levi-Civita symbol
eijk = np.zeros((3, 3, 3))
eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1

def scalar_triple(a, b, c):
    #return a.dot(np.cross(b, c)) 
    return np.einsum('ijk,i,j,k->', eijk, a, b, c)

def omega_simple(l, w, h): # corner at (0, 0, 0), point at (0, 0, h)
    return np.arctan((l * w) / (h * np.sqrt(l ** 2 + w ** 2 + h ** 2)))  

def triangle_sa(R1, R2, R3):
    l = np.linalg.norm(np.vstack((R1, R2, R3)), axis=1)
    p = np.array([R2.dot(R3), R1.dot(R3), R1.dot(R2)]) 

    N = scalar_triple(R1, R2, R3)
    D = l.prod() + l.dot(p)

    return 2. * np.arctan2(N, D)

class RectangularFacet(object):
    def __init__(self, corner, r1, r2, sense=1.0, name=None):
        self.name = name
        self.corner = corner
        self.r1 = r1
        self.r2 = r2

        # Normal vector
        self.sense = sense
        self.n = np.cross(self.r1, self.r2)
        self.n /= np.linalg.norm(self.n)
        self.n *= sense 

        # These are the vectors in terms of the Van Oosterom definitions
        self.a = self.corner
        self.a_p = self.corner + self.r1 + self.r2
        self.b = self.corner + self.r1
        self.c = self.corner + self.r2

        self._V = np.vstack((self.a, self.a_p, self.b, self.c))

        # self.b_p = self.corner + self.r2
        # self.c_p = self.corner + self.r1

    @property
    def edges(self):
        return np.vstack((self.r1, self.r2))

    def is_facing(self, P):
        if self.n.dot(P - self.c) > 0.0: return True
        else: return False 

    def __call__(self, P):
        a, a_p, b, c = self._V - P

        return -self.sense * (triangle_sa(a, b, c) + triangle_sa(a_p, c, b))
