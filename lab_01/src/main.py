#!/usr/bin/env python3
"""
Главный скрипт лабораторной работы.
Запускает полный цикл: чтение данных -> интерполяция -> решение -> вывод.
"""


def main():
    # 1. Загружаем конфигурацию
    import config

    # 2. Читаем исходные данные
    from file_reader import read_all_data
    raw_data = read_all_data('data/data.txt')

    # 3. Создаём интерполяторы для всех таблиц
    from interpolation import interpolate_1d, interpolate_2d

    # Функции-интерполяторы с "зашитыми" данными (замыкание)
    def current_interpolator(t):
        return interpolate_1d(raw_data['current']['time'],
                              raw_data['current']['current'],
                              t, degree=3)

    def nh_interpolator(t, p):
        return interpolate_2d(raw_data['nh']['temperatures'],
                              raw_data['nh']['pressures'],
                              raw_data['nh']['values'],
                              t, p, t_degree=2, p_degree=2)

    def sigma_interpolator(t, p):
        return interpolate_2d(raw_data['sigma']['temperatures'],
                              raw_data['sigma']['pressures'],
                              raw_data['sigma']['values'],
                              t, p, t_degree=2, p_degree=2)

    # ... аналогично для q и c

    # 4. Решаем ОДУ
    from solver import solve_temperature
    tables = {
        'nh': nh_interpolator,
        'sigma': sigma_interpolator,
        'q': q_interpolator,
        'c': c_interpolator
    }

    solution = solve_temperature(
        t_span=(config.T0_TIME, config.TK_TIME),
        tau=config.TAU,
        initial_temp=config.T0,
        current_interpolator=current_interpolator,
        tables=tables,
        config=config
    )

    # 5. Рассчитываем дополнительные величины
    from calculator import compute_derived_quantities, compute_statistics
    full_solution = compute_derived_quantities(
        solution, sigma_interpolator, q_interpolator, config
    )
    stats = compute_statistics(full_solution)

    # 6. Выводим результаты
    from visualizer import print_results_table, plot_all_quantities
    print_results_table(full_solution, filename='output/results.txt')
    print("Статистика:", stats)
    plot_all_quantities(full_solution, save_path='output/plots/')

    print("Расчёт завершён успешно!")


if __name__ == "__main__":
    main()