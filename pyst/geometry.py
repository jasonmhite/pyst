import numpy as np

__all__ = ["RotationMatrix", "align_vectors"]

class RotationMatrix(object):

    __inverse = None

    def __init__(self, R):
        self._R = R

    @classmethod
    def rot(cls, theta, direction):
        R = None

        if direction == "x":
            R = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ]) 
            
        elif direction == "y":
            R = np.array([
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]
            ])
        
        elif direction == "z":
            R = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])

        else: raise ValueError("Must provide angle and axis")

        return cls(R)

    def __lshift__(self, other): # Apply other, then self
        R = self._R.dot(other._R)
        return RotationMatrix(R)

    def __rshift__(self, other): # Self, then other
        R = other._R.dot(self._R)
        return RotationMatrix(R)
    
    def __call__(self, X):
        if X.ndim == 1: 
            return self._R.dot(X)
        else:
            return np.einsum(
                "ij,kj->ki",
                self._R,
                X,
            )

    @property
    def inv(self):
        if self.__inverse is None:
            self.__inverse = RotationMatrix(np.linalg.inv(self._R))

        return self.__inverse

def align_vectors(a, b):
    # Returns the rotation matrix that rotates a onto b
    # via https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d 
    # alt https://stackoverflow.com/questions/45142959/calculate-rotation-matrix-to-align-two-vectors-in-3d-space

    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)

    if a.dot(b) == 1.0:
        return RotationMatrix(np.eye(3))

    v = np.cross(a, b)
    c = a.dot(b)
    s = np.linalg.norm(v)

    Vx = np.array([
        [    0, -v[2],  v[1]],
        [ v[2],     0, -v[0]],
        [-v[1],  v[0],     0],
    ])

    #return RotationMatrix(np.eye(3) + Vx + ((1. - c) / (s ** 2)) * (Vx.dot(Vx)))
    return RotationMatrix(np.eye(3) + Vx + ((1. - c) / (s ** 2)) * np.matmul(Vx, Vx))
