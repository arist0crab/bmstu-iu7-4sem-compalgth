import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from filereader import load_all_data
from interpolation import create_interpolators
from models import compute_current_density
from solver import solve_ode
from calculator import compute_derived_quantities, compute_statistics
from visualizer import create_visualizer


class Config:
    R_TUBE = 0.25
    L_TUBE = 12.0
    TAU = 1e-6
    T0 = 5400.0
    T0_TIME = 14e-6
    TK_TIME = 450e-6
    PRESSURE_BRACKET = [0.3, 2.5]
    NH_CONST = 7.242e4 * 0.04 / 300.0


def main():
    data_path = Path(__file__).parent.parent / 'data' / 'data.txt'
    raw_data = load_all_data(str(data_path))
    interpolators = create_interpolators(raw_data)

    def current_density_func(t):
        current = interpolators['current'](t)
        return compute_current_density(current, Config.R_TUBE)

    solution = solve_ode(
        (Config.T0_TIME, Config.TK_TIME),
        Config.TAU,
        Config.T0,
        current_density_func,
        interpolators,
        Config
    )

    solution = compute_derived_quantities(
        solution,
        interpolators['sigma'],
        interpolators['q'],
        Config
    )

    stats = compute_statistics(solution)

    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    visualize = create_visualizer(output_dir=str(output_dir))
    files = visualize(solution, stats, prefix='final_')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--no-plot', action='store_true')

    args = parser.parse_args()

    if args.no_plot:
        import matplotlib

        matplotlib.use('Agg')

    main()
