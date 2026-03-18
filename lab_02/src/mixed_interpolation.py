import numpy as np
from newton import newton_1d, newton_2d
from spline import cubic_spline_1d, cubic_spline_2d


def mixed_2d(x_nodes, y_nodes, values_2d, x_star, y_star, method_x, method_y, nx=None, ny=None):
    interpolations = []

    for j in range(len(y_nodes)):
        if method_x == 'newton':
            val = newton_1d(x_nodes[:nx + 1], values_2d[j, :nx + 1], x_star)
        else:
            val = cubic_spline_1d(x_nodes, values_2d[j, :], x_star)
        interpolations.append(val)

    if method_y == 'newton':
        return newton_1d(y_nodes[:ny + 1], interpolations[:ny + 1], y_star)
    else:
        return cubic_spline_1d(y_nodes, interpolations, y_star)


def mixed_3d(x_nodes, y_nodes, z_nodes, values_3d, x_star, y_star, z_star,
             method_x, method_y, method_z, nx=None, ny=None, nz=None):
    interpolations = []

    for k in range(len(z_nodes)):
        xy_slice = values_3d[k, :, :]
        val = mixed_2d(x_nodes, y_nodes, xy_slice, x_star, y_star, method_x, method_y, nx, ny)
        interpolations.append(val)

    if method_z == 'newton':
        return newton_1d(z_nodes[:nz + 1], interpolations[:nz + 1], z_star)
    else:
        return cubic_spline_1d(z_nodes, interpolations, z_star)