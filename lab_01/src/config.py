import numpy as np

# Физические константы
BOLTZMANN = 1.38e-23
R_TUBE = 0.25
L_TUBE = 12.0

# Параметры для отладки
T0 = 5400.0
T0_TIME = 14e-6
TK_TIME = 450e-6
PX = 0.04
TX = 300.0

# Численные параметры
TAU = 1e-6
PRESSURE_BRACKET = [0.3, 2.5]
NH_CONST = 7.242e4 * PX / TX

# Параметры интерполяции
INTERP_DEGREE_T = 2
INTERP_DEGREE_P = 2
INTERP_DEGREE_TIME = 3