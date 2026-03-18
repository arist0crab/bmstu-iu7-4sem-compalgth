import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import load_interpolation_data
from src.interpolator import Interpolator3D


def main():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'data_lab2.txt')
    x_nodes, y_nodes, z_nodes, values_3d = load_interpolation_data(file_path)

    print("Лабораторная работа: трёхмерная интерполяция")
    print(f"Сетка: {len(x_nodes)}x{len(y_nodes)}x{len(z_nodes)}")
    print(f"x: {x_nodes}")
    print(f"y: {y_nodes}")
    print(f"z: {z_nodes}")

    interpolator = Interpolator3D(x_nodes, y_nodes, z_nodes, values_3d)

    test_points = [(1.5, 1.5, 1.5), (2.5, 2.5, 2.5), (1.5, 2.5, 3.5)]

    print("\nРезультаты интерполяции:")

    for x, y, z in test_points:
        print(f"\nТочка ({x}, {y}, {z})")
        n_result = interpolator.newton(x, y, z, 2, 2, 2)
        s_result = interpolator.spline(x, y, z)
        m1_result = interpolator.mixed(x, y, z, 'newton', 'spline', 'spline', 2, None, None)
        m2_result = interpolator.mixed(x, y, z, 'spline', 'newton', 'spline', None, 2, None)
        m3_result = interpolator.mixed(x, y, z, 'spline', 'spline', 'newton', None, None, 2)

        print(f"  Ньютон (2,2,2):      {n_result:.4f}")
        print(f"  Сплайн:              {s_result:.4f}")
        print(f"  Смешанный (Н,С,С):   {m1_result:.4f}")
        print(f"  Смешанный (С,Н,С):   {m2_result:.4f}")
        print(f"  Смешанный (С,С,Н):   {m3_result:.4f}")

    print("\nПроверка в узлах:")
    for x in [0, 2, 4]:
        for y in [0, 2, 4]:
            for z in [0, 2, 4]:
                result = interpolator.spline(x, y, z)
                expected = x * x + y * y + z * z
                print(f"f({x},{y},{z}) = {result:6.1f} (ожидаемо {expected:6.1f})")


if __name__ == "__main__":
    main()