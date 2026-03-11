import numpy as np


def pressure_equation(nh_interp, temperature, pressure, nh_const):
    return nh_interp(temperature, pressure) - nh_const


def compute_current_density(current, radius):
    return current / (np.pi * radius * radius)


def compute_phi(current_density, sigma, q, c):
    return (current_density * current_density / sigma - q) / c


def compute_resistance(sigma, length, radius):
    return length / (np.pi * sigma * radius * radius)


def compute_radiation_flux(q, radius):
    return q * radius / 2.0


def compute_joule_heating(current_density, sigma):
    return current_density * current_density / sigma


def create_model_functions(interpolators, config):
    def get_current_density(t):
        current = interpolators['current'](t)
        return compute_current_density(current, config.R_TUBE)

    def get_pressure_from_temperature(temperature, pressure_guess=None):
        if pressure_guess is None:
            pressure_guess = config.PRESSURE_BRACKET[0]
        return pressure_guess

    def get_sigma(temperature, pressure):
        return interpolators['sigma'](temperature, pressure)

    def get_q(temperature, pressure):
        return interpolators['q'](temperature, pressure)

    def get_c(temperature, pressure):
        return interpolators['c'](temperature, pressure)

    def get_nh(temperature, pressure):
        return interpolators['nh'](temperature, pressure)

    def compute_rhs(t, temperature, pressure, current_density=None):
        if current_density is None:
            current_density = get_current_density(t)

        sigma = get_sigma(temperature, pressure)
        q = get_q(temperature, pressure)
        c = get_c(temperature, pressure)

        return compute_phi(current_density, sigma, q, c)

    return {
        'get_current_density': get_current_density,
        'get_sigma': get_sigma,
        'get_q': get_q,
        'get_c': get_c,
        'get_nh': get_nh,
        'compute_rhs': compute_rhs,
        'compute_resistance': lambda t, p: compute_resistance(
            get_sigma(t, p), config.L_TUBE, config.R_TUBE
        ),
        'compute_flux': lambda t, p: compute_radiation_flux(
            get_q(t, p), config.R_TUBE
        )
    }
