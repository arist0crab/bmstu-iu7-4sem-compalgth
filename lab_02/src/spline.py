import numpy as np


def cubic_spline_1d(x_nodes, y_nodes, x_star):
    n = len(x_nodes)
    h = x_nodes[1] - x_nodes[0]

    a = y_nodes.copy()
    b = np.zeros(n - 1)
    c = np.zeros(n)
    d = np.zeros(n - 1)

    _compute_spline_coefficients(a, b, c, d, n, h)

    interval = _find_interval(x_nodes, x_star)
    if interval >= n - 1:
        interval = n - 2

    dx = x_star - x_nodes[interval]

    return a[interval] + b[interval] * dx + c[interval] * dx ** 2 + d[interval] * dx ** 3


def cubic_spline_2d(x_nodes, y_nodes, values_2d, x_star, y_star):
    nx = len(x_nodes)
    ny = len(y_nodes)

    splines_at_y = []

    for j in range(ny):
        splines_at_y.append(cubic_spline_1d(x_nodes, values_2d[j, :], x_star))

    return cubic_spline_1d(y_nodes, splines_at_y, y_star)


def cubic_spline_3d(x_nodes, y_nodes, z_nodes, values_3d, x_star, y_star, z_star):
    nz = len(z_nodes)

    splines_at_z = []

    for k in range(nz):
        splines_at_z.append(cubic_spline_2d(x_nodes, y_nodes, values_3d[k, :, :], x_star, y_star))

    return cubic_spline_1d(z_nodes, splines_at_z, z_star)


def _compute_spline_coefficients(a, b, c, d, n, h):
    alpha = np.zeros(n)
    beta = np.zeros(n)

    alpha[0] = 0
    beta[0] = 0

    for i in range(1, n - 1):
        A = h
        B = 4 * h
        C = h
        F = 3 * (a[i + 1] - 2 * a[i] + a[i - 1]) / h

        denominator = A * alpha[i - 1] + B
        alpha[i] = -C / denominator
        beta[i] = (F - A * beta[i - 1]) / denominator

    c[n - 1] = 0

    for i in range(n - 2, -1, -1):
        c[i] = alpha[i] * c[i + 1] + beta[i]

    for i in range(n - 1):
        b[i] = (a[i + 1] - a[i]) / h - h * (c[i + 1] + 2 * c[i]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h)


def _find_interval(x_nodes, x_star):
    for i in range(len(x_nodes) - 1):
        if x_star <= x_nodes[i + 1]:
            return i
    return len(x_nodes) - 2