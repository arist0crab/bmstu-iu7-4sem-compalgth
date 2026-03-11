from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _can_show_plots():
    """Проверяет, можно ли показывать графики интерактивно"""
    try:
        import matplotlib
        return matplotlib.get_backend().lower() != 'agg'
    except:
        return False


def print_statistics(stats):
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА РАСЧЁТА")
    print("=" * 60)

    print(f"\n  Температура:")
    print(f"    Максимальная: {stats['T_max']:.1f} K при t={stats['T_max_time']:.1f} мкс")
    print(f"    Минимальная:  {stats['T_min']:.1f} K при t={stats['T_min_time']:.1f} мкс")

    print(f"\n  Давление:")
    print(f"    Максимальное: {stats['p_max']:.3f} МПа при t={stats['p_max_time']:.1f} мкс")
    print(f"    Минимальное:  {stats['p_min']:.3f} МПа")

    print(f"\n  Электропроводность:")
    print(f"    Максимальная: {stats['sigma_max']:.2e} 1/(Ом·см) при t={stats['sigma_max_time']:.1f} мкс")

    print(f"\n  Мощность излучения:")
    print(f"    Максимальная: {stats['q_max']:.2e} Вт/см³ при t={stats['q_max_time']:.1f} мкс")

    print(f"\n  Сопротивление:")
    print(f"    Минимальное:  {stats['resistance_min']:.3f} Ом при t={stats['resistance_min_time']:.1f} мкс")
    print(f"    Максимальное: {stats['resistance_max']:.3f} Ом")

    print(f"\n  Поток излучения:")
    print(f"    Максимальный: {stats['flux_max']:.2e} Вт/см² при t={stats['flux_max_time']:.1f} мкс")


def print_table(solution, n_rows=20):
    t = solution['time']
    T = solution['temperature']
    p = solution['pressure']
    sigma = solution.get('sigma', np.zeros_like(t))
    q = solution.get('q', np.zeros_like(t))
    resistance = solution.get('resistance', np.zeros_like(t))
    flux = solution.get('flux', np.zeros_like(t))

    print("\n" + "=" * 100)
    print(
        f"{'t, мкс':>10} {'T, K':>12} {'p, МПа':>10} {'σ, 1/(Ом·см)':>16} {'q, Вт/см³':>12} {'Rd, Ом':>10} {'Fr, Вт/см²':>12}")
    print("=" * 100)

    step = max(1, len(t) // n_rows)

    for i in range(0, len(t), step):
        print(f"{t[i] * 1e6:10.2f} "
              f"{T[i]:12.1f} "
              f"{p[i]:10.3f} "
              f"{sigma[i]:16.2e} "
              f"{q[i]:12.2e} "
              f"{resistance[i]:10.3f} "
              f"{flux[i]:12.2e}")


def save_table(solution, filename):
    t = solution['time']
    T = solution['temperature']
    p = solution['pressure']
    sigma = solution.get('sigma', np.zeros_like(t))
    q = solution.get('q', np.zeros_like(t))
    resistance = solution.get('resistance', np.zeros_like(t))
    flux = solution.get('flux', np.zeros_like(t))

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, 'w') as f:
        f.write("# t(мкс)  T(K)  p(МПа)  sigma(1/(Ом·см))  q(Вт/см³)  Rd(Ом)  Fr(Вт/см²)\n")
        for i in range(len(t)):
            f.write(
                f"{t[i] * 1e6:.4f} {T[i]:.1f} {p[i]:.6f} {sigma[i]:.6e} {q[i]:.6e} {resistance[i]:.6f} {flux[i]:.6e}\n")


def plot_all(solution, save_path=None):
    t_us = solution['time'] * 1e6
    T = solution['temperature']
    p = solution['pressure']
    sigma = solution.get('sigma', np.zeros_like(t_us))
    q = solution.get('q', np.zeros_like(t_us))
    resistance = solution.get('resistance', np.zeros_like(t_us))
    flux = solution.get('flux', np.zeros_like(t_us))

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].plot(t_us, T, 'b-', linewidth=1.5)
    axes[0, 0].set_xlabel('t, мкс')
    axes[0, 0].set_ylabel('T, K')
    axes[0, 0].set_title('Температура плазмы')
    axes[0, 0].grid(True, alpha=0.3)

    T_max_idx = np.argmax(T)
    axes[0, 0].plot(t_us[T_max_idx], T[T_max_idx], 'ro', markersize=6)
    axes[0, 0].annotate(f'{T[T_max_idx]:.0f} K',
                        xy=(t_us[T_max_idx], T[T_max_idx]),
                        xytext=(10, 10), textcoords='offset points')

    axes[0, 1].plot(t_us, p, 'r-', linewidth=1.5)
    axes[0, 1].set_xlabel('t, мкс')
    axes[0, 1].set_ylabel('p, МПа')
    axes[0, 1].set_title('Давление плазмы')
    axes[0, 1].grid(True, alpha=0.3)

    p_max_idx = np.argmax(p)
    axes[0, 1].plot(t_us[p_max_idx], p[p_max_idx], 'ro', markersize=6)
    axes[0, 1].annotate(f'{p[p_max_idx]:.3f} МПа',
                        xy=(t_us[p_max_idx], p[p_max_idx]),
                        xytext=(10, 10), textcoords='offset points')

    axes[0, 2].plot(t_us, sigma, 'g-', linewidth=1.5)
    axes[0, 2].set_xlabel('t, мкс')
    axes[0, 2].set_ylabel('σ, 1/(Ом·см)')
    axes[0, 2].set_title('Электропроводность')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].set_yscale('log')

    axes[1, 0].plot(t_us, q, 'm-', linewidth=1.5)
    axes[1, 0].set_xlabel('t, мкс')
    axes[1, 0].set_ylabel('q, Вт/см³')
    axes[1, 0].set_title('Мощность излучения')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_yscale('log')

    axes[1, 1].plot(t_us, resistance, 'c-', linewidth=1.5)
    axes[1, 1].set_xlabel('t, мкс')
    axes[1, 1].set_ylabel('Rd, Ом')
    axes[1, 1].set_title('Сопротивление')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_yscale('log')

    Rd_min_idx = np.argmin(resistance)
    axes[1, 1].plot(t_us[Rd_min_idx], resistance[Rd_min_idx], 'ro', markersize=6)
    axes[1, 1].annotate(f'{resistance[Rd_min_idx]:.3f} Ом',
                        xy=(t_us[Rd_min_idx], resistance[Rd_min_idx]),
                        xytext=(10, -15), textcoords='offset points')

    axes[1, 2].plot(t_us, flux, 'y-', linewidth=1.5)
    axes[1, 2].set_xlabel('t, мкс')
    axes[1, 2].set_ylabel('Fr, Вт/см²')
    axes[1, 2].set_title('Поток излучения')
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].set_yscale('log')

    flux_max_idx = np.argmax(flux)
    axes[1, 2].plot(t_us[flux_max_idx], flux[flux_max_idx], 'ro', markersize=6)
    axes[1, 2].annotate(f'{flux[flux_max_idx]:.2e} Вт/см²',
                        xy=(t_us[flux_max_idx], flux[flux_max_idx]),
                        xytext=(10, 10), textcoords='offset points')

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n  Графики сохранены в: {save_path}")

    if _can_show_plots():
        plt.show()
    else:
        plt.close(fig)


def plot_phase_diagram(solution, save_path=None):
    t_us = solution['time'] * 1e6
    T = solution['temperature']
    p = solution['pressure']

    fig, ax = plt.subplots(figsize=(8, 6))

    scatter = ax.scatter(T, p, c=t_us, cmap='viridis', s=10, alpha=0.7)
    ax.plot(T, p, 'k-', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('T, K')
    ax.set_ylabel('p, МПа')
    ax.set_title('Фазовая траектория (T-p)')
    ax.grid(True, alpha=0.3)

    cbar = plt.colorbar(scatter)
    cbar.set_label('t, мкс')

    ax.plot(T[0], p[0], 'go', markersize=8, label='Старт')
    ax.plot(T[-1], p[-1], 'ro', markersize=8, label='Финиш')
    ax.legend()

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n  Фазовая диаграмма сохранена в: {save_path}")

    if _can_show_plots():
        plt.show()
    else:
        plt.close(fig)


def create_visualizer(output_dir='output'):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    def visualize(solution, stats, prefix=''):
        print_statistics(stats)
        print_table(solution)

        table_file = f"{output_dir}/{prefix}results.txt"
        save_table(solution, table_file)
        print(f"\n  Таблица сохранена в: {table_file}")

        plots_file = f"{output_dir}/{prefix}plots.png"
        plot_all(solution, plots_file)

        phase_file = f"{output_dir}/{prefix}phase.png"
        plot_phase_diagram(solution, phase_file)

        return {
            'table_file': table_file,
            'plots_file': plots_file,
            'phase_file': phase_file
        }

    return visualize
