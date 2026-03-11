import numpy as np


def find_pressure(temperature, nh_interp, nh_const, pressure_bracket, max_iter=100):
    a, b = pressure_bracket
    fa = nh_interp(temperature, a) - nh_const
    fb = nh_interp(temperature, b) - nh_const

    if fa * fb > 0:
        return a

    for _ in range(max_iter):
        c = (a + b) * 0.5
        fc = nh_interp(temperature, c) - nh_const

        if abs(fc) < 1e-10:
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return (a + b) * 0.5


def rk2_step(t, T, tau, current_density_func, nh_interp, sigma_interp, q_interp, c_interp, config):
    j = current_density_func(t)

    p_n = find_pressure(T, nh_interp, config.NH_CONST, config.PRESSURE_BRACKET)

    sigma_n = sigma_interp(T, p_n)
    q_n = q_interp(T, p_n)
    c_n = c_interp(T, p_n)

    phi_n = (j * j / sigma_n - q_n) / c_n

    T_half = T + 0.5 * tau * phi_n

    p_half = find_pressure(T_half, nh_interp, config.NH_CONST, config.PRESSURE_BRACKET)

    sigma_half = sigma_interp(T_half, p_half)
    q_half = q_interp(T_half, p_half)
    c_half = c_interp(T_half, p_half)

    phi_half = (j * j / sigma_half - q_half) / c_half

    T_next = T + tau * phi_half

    return T_next, p_n, p_half, sigma_n, q_n


def solve_ode(t_span, tau, T0, current_density_func, interpolators, config):
    t_start, t_end = t_span
    n_steps = int((t_end - t_start) / tau) + 1

    t_array = np.linspace(t_start, t_end, n_steps)
    T_array = np.zeros(n_steps)
    p_array = np.zeros(n_steps)
    sigma_array = np.zeros(n_steps)
    q_array = np.zeros(n_steps)

    T_array[0] = T0
    p_array[0] = find_pressure(T0, interpolators['nh'], config.NH_CONST, config.PRESSURE_BRACKET)

    for i in range(n_steps - 1):
        T_next, p_n, p_half, sigma_n, q_n = rk2_step(
            t_array[i], T_array[i], tau,
            current_density_func,
            interpolators['nh'],
            interpolators['sigma'],
            interpolators['q'],
            interpolators['c'],
            config
        )

        T_array[i + 1] = T_next
        p_array[i + 1] = p_half
        sigma_array[i + 1] = sigma_n
        q_array[i + 1] = q_n

    return {
        'time': t_array,
        'temperature': T_array,
        'pressure': p_array,
        'sigma': sigma_array,
        'q': q_array
    }


def create_solver(config):
    def solve(t_span, T0, current_density_func, interpolators):
        return solve_ode(
            t_span, config.TAU, T0,
            current_density_func, interpolators, config
        )

    return solve
