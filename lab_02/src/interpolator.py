import numpy as np

from mixed_interpolation import mixed_3d
from newton import newton_3d
from spline import cubic_spline_3d


class Interpolator3D:
    def __init__(self, x_nodes, y_nodes, z_nodes, values_3d):
        self.x_nodes = np.array(x_nodes)
        self.y_nodes = np.array(y_nodes)
        self.z_nodes = np.array(z_nodes)
        self.values_3d = values_3d

    def newton(self, x, y, z, nx, ny, nz):
        return newton_3d(self.x_nodes, self.y_nodes, self.z_nodes, self.values_3d, x, y, z, nx, ny, nz)

    def spline(self, x, y, z):
        return cubic_spline_3d(self.x_nodes, self.y_nodes, self.z_nodes, self.values_3d, x, y, z)

    def mixed(self, x, y, z, method_x, method_y, method_z, nx=None, ny=None, nz=None):
        return mixed_3d(self.x_nodes, self.y_nodes, self.z_nodes, self.values_3d, x, y, z, method_x, method_y, method_z, nx, ny, nz)
