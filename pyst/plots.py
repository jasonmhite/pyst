import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot_vector(r, x0=None, ax=None, *args, **kwargs):
    if ax is None: ax = plt.gca()
    if x0 is None: x0 = np.zeros(3)

    if "mutation_scale" not in kwargs:
        kwargs["mutation_scale"] = 20
    if "arrowstyle" not in kwargs:
        kwargs["arrowstyle"] = "->"

    xs, ys, zs = np.column_stack((x0, r))

    a = Arrow3D(
        xs,
        ys,
        zs,
        *args,
        **kwargs
    )

    ax.add_artist(a)

def plot_facet(F, ax=None, normal=True, normal_len=1.0, normal_kwargs={}, *args, **kwargs):
    if ax is None:
        ax = plt.gca()

    verts = np.array([[
        F.c,
        F.c + F.r1,
        F.c + F.r1 + F.r2,
        F.c + F.r2,
    ]])

    ax.add_collection3d(Poly3DCollection(verts, *args, **kwargs))

    if normal:
        cm = F.c + 0.5 * (F.r1 + F.r2)
        plot_vector(cm + normal_len * F.n, x0=cm, ax=ax, **normal_kwargs)
