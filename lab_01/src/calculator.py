import numpy as np


def compute_resistance(sigma, length, radius):
    return length / (np.pi * sigma * radius * radius)


def compute_radiation_flux(q, radius):
    return q * radius / 2.0


def compute_derived_quantities(solution, sigma_interp, q_interp, config):
    n = len(solution['time'])
    
    resistance = np.zeros(n)
    flux = np.zeros(n)
    
    for i in range(n):
        sigma_val = sigma_interp(solution['temperature'][i], solution['pressure'][i])
        q_val = q_interp(solution['temperature'][i], solution['pressure'][i])
        
        resistance[i] = compute_resistance(sigma_val, config.L_TUBE, config.R_TUBE)
        flux[i] = compute_radiation_flux(q_val, config.R_TUBE)
    
    solution['resistance'] = resistance
    solution['flux'] = flux
    
    return solution


def compute_statistics(solution):
    t = solution['time']
    T = solution['temperature']
    p = solution['pressure']
    sigma = solution.get('sigma', np.zeros_like(t))
    q = solution.get('q', np.zeros_like(t))
    resistance = solution.get('resistance', np.zeros_like(t))
    flux = solution.get('flux', np.zeros_like(t))
    
    T_max_idx = np.argmax(T)
    p_max_idx = np.argmax(p)
    
    stats = {
        'T_max': np.max(T),
        'T_max_time': t[T_max_idx] * 1e6,
        'T_min': np.min(T),
        'T_min_time': t[np.argmin(T)] * 1e6,
        
        'p_max': np.max(p),
        'p_max_time': t[p_max_idx] * 1e6,
        'p_min': np.min(p),
        
        'sigma_max': np.max(sigma),
        'sigma_max_time': t[np.argmax(sigma)] * 1e6,
        
        'q_max': np.max(q),
        'q_max_time': t[np.argmax(q)] * 1e6,
        
        'resistance_min': np.min(resistance),
        'resistance_min_time': t[np.argmin(resistance)] * 1e6,
        'resistance_max': np.max(resistance),
        
        'flux_max': np.max(flux),
        'flux_max_time': t[np.argmax(flux)] * 1e6,
    }
    
    return stats


def compute_integrals(solution, config):
    t = solution['time']
    T = solution['temperature']
    q = solution.get('q', np.zeros_like(t))
    
    dt = t[1] - t[0]
    
    total_energy = np.sum(q) * dt
    average_temperature = np.mean(T)
    
    return {
        'total_radiated_energy': total_energy,
        'average_temperature': average_temperature,
        'time_steps': len(t),
        'total_time': t[-1] - t[0]
    }


def create_calculator(config):
    def calculate(solution, sigma_interp, q_interp):
        return compute_derived_quantities(solution, sigma_interp, q_interp, config)
    
    return calculate