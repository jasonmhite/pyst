import numpy as np

from .geometry import *

def omega_simple(l, w, h): # corner at (0, 0, 0), point at (0, 0, h)
    return np.arctan((l * w) / (h * np.sqrt(l ** 2 + w ** 2 + h ** 2)))


def omega(x_1, x_2, y_1, y_2, x_p, y_p, z_p):
    A = np.array([
        (x_2 - x_p) * (y_2 - y_p),
        (x_1 - x_p) * (y_2 - y_p),
        (x_2 - x_p) * (y_1 - y_p),
        (x_1 - x_p) * (y_1 - y_p),
    ])
    
    B = np.array([
        (x_2 - x_p) ** 2 + (y_2 - y_p) ** 2 + z_p ** 2,
        (x_1 - x_p) ** 2 + (y_2 - y_p) ** 2 + z_p ** 2,
        (x_2 - x_p) ** 2 + (y_1 - y_p) ** 2 + z_p ** 2,
        (x_1 - x_p) ** 2 + (y_1 - y_p) ** 2 + z_p ** 2,
    ]) 
    
    B = np.sqrt(B)
    B *= z_p
    
    C = np.arctan(A / B)
    # C = np.arctan2(A, B)
    
    return C.dot(np.array([1, -1, -1, 1]))

class RectangularFacet(object):

    # corner, edge vectors
    # Probably need normal vector too for sense
    def __init__(self, c, r1, r2, sense, name=None):
        self.name = name
        self.c = c
        self.r1 = r1
        self.r2 = r2

        # Normal vector
        self.sense = sense
        self.n = np.cross(self.r1, self.r2)
        self.n /= np.linalg.norm(self.n)
        # self.n *= sense

        if not np.cross(self.r1, np.array([0, 1, 0])).any(): 
            # Already aligned to y axis, need to swap (not sure if really needed)

            # These need to be verified...
            self.r1, self.r2 = self.r2, self.r1
            self._R = RotationMatrix(np.eye(3)[[1, 0, 2]])
            self.sense *= -1
            self.n *= -1

        elif not np.cross(self.r1, np.array([1, 0, 0])).any():
            self._R = RotationMatrix(np.eye(3))

        else:
            R1 = align_vectors(
                self.n,
                np.array([0, 0, 1.0]),
            )

            R2 = align_vectors(
                R1(self.r1),
                np.array([1.0, 0, 0])
            )

            self._R = R2 << R1

        # self._x1, self._y1, _, self._x2, self._y2, _ = self._R(
            # np.vstack((self.r1, self.r2))
        # ).flatten() 

        self._x1, self._y1, _, self._x2, self._y2, _ = self._R(
            np.vstack((self.c + self.r1, self.c + self.r2))
        ).flatten()  

    @property
    def edges(self):
        return np.vstack((self.r1, self.r2))

    def is_facing(self, P):
        if self.n.dot(P) > 0.0: return True
        else: return False

    def __call__(self, P):
        #Translate P to relative frame

        P0 = self._R(P) - self.c

        # Not sure why negative...
        return self.sense * omega(
            self._x1,
            self._x2,
            self._y1,
            self._y2,
            *P0
        )
