"""
Модуль для расчёта дополнительных характеристик.
"""


def compute_derived_quantities(solution, sigma_interpolator, q_interpolator, config):
    """
    По полученному решению рассчитывает:
        - Rd(t) - сопротивление
        - Fr(t) - поток излучения

    Args:
        solution: результат из solver.solve_temperature
        sigma_interpolator: функция для sigma(T,p)
        q_interpolator: функция для q(T,p)
        config: конфигурация (R, l)

    Returns:
        dict: дополненное решение с полями:
            'resistance': array[...]
            'flux': array[...]
    """
    pass


def compute_statistics(solution):
    """
    Вычисляет статистики:
        - максимальная температура
        - максимальное давление
        - время достижения максимумов
        - полная энергия и т.д.
    """
    pass