"""
Модуль физических моделей.
Функции, представляющие уравнения (1)-(3) из задания.
"""


def compute_nh_constant(px, tx):
    """
    Вычисляет константу из уравнения (3):
    const = 7.242e4 * px / tx
    """
    pass


def pressure_equation(nh_func, t, p, nh_const):
    """
    Уравнение (5) для поиска давления:
    f(p) = Nh(T, p) - nh_const = 0

    Args:
        nh_func: функция двумерной интерполяции Nh(T, p)
        t: температура
        p: давление (переменная)
        nh_const: константа из уравнения (3)

    Returns:
        float: значение невязки
    """
    pass


def compute_phi(j, sigma, q, c):
    """
    Вычисляет правую часть дифференциального уравнения:
    phi = (j^2/sigma - q) / c
    """
    pass


def current_density(i, radius):
    """Плотность тока: j = I / (pi * R^2)"""
    pass


def resistance(sigma, length, radius):
    """Сопротивление: Rd = l / (pi * sigma * R^2)"""
    pass


def radiation_flux(q, radius):
    """Поток излучения: Fr = q * R / 2"""
    pass