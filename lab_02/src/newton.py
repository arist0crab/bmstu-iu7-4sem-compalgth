import numpy as np


def newton_1d(x_nodes, y_nodes, x_star):
    n = len(x_nodes)
    divided_diffs = _compute_divided_differences(x_nodes, y_nodes)

    result = divided_diffs[0]
    product = 1.0

    for i in range(1, n):
        product *= (x_star - x_nodes[i - 1])
        result += divided_diffs[i] * product

    return result


def newton_2d(x_nodes, y_nodes, values_2d, x_star, y_star, nx, ny):
    x_interpolations = []

    for j in range(ny + 1):
        y_slice = values_2d[j, :]
        x_interpolations.append(newton_1d(x_nodes[:nx + 1], y_slice[:nx + 1], x_star))

    return newton_1d(y_nodes[:ny + 1], x_interpolations, y_star)


def newton_3d(x_nodes, y_nodes, z_nodes, values_3d, x_star, y_star, z_star, nx, ny, nz):
    xy_interpolations = []

    for k in range(nz + 1):
        xy_slice = values_3d[k, :ny + 1, :nx + 1]
        xy_interpolations.append(newton_2d(x_nodes[:nx + 1], y_nodes[:ny + 1], xy_slice, x_star, y_star, nx, ny))

    return newton_1d(z_nodes[:nz + 1], xy_interpolations, z_star)


def _compute_divided_differences(x_nodes, y_nodes):
    n = len(x_nodes)
    f = np.zeros((n, n))
    f[:, 0] = y_nodes

    for j in range(1, n):
        for i in range(n - j):
            f[i, j] = (f[i + 1, j - 1] - f[i, j - 1]) / (x_nodes[i + j] - x_nodes[i])

    return f[0, :]