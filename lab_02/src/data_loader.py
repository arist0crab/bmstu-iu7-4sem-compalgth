import numpy as np


def load_interpolation_data(filename):
    lines = _read_file_lines(filename)
    z_nodes, values_3d = _parse_interpolation_blocks(lines)

    x_nodes = np.array([0, 1, 2, 3, 4])
    y_nodes = np.array([0, 1, 2, 3, 4])
    return x_nodes, y_nodes, z_nodes, values_3d


def get_xy_slice(values_3d, z_index):
    return values_3d[z_index, :, :]


def get_x_line(values_3d, y_index, z_index):
    return values_3d[z_index, y_index, :]


def get_y_line(values_3d, x_index, z_index):
    return values_3d[z_index, :, x_index]


def get_z_line(values_3d, x_index, y_index):
    return values_3d[:, y_index, x_index]


def _read_file_lines(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def _parse_interpolation_blocks(lines):
    z_nodes = []
    values_3d = []
    current_matrix = []

    for line in lines:
        if line.startswith('z='):
            if current_matrix:
                values_3d.append(np.array(current_matrix))
            z_nodes.append(_parse_z_value(line))
            current_matrix = []
        elif line.startswith('y\\x'):
            continue
        else:
            row = _parse_data_row(line)
            if row is not None:
                current_matrix.append(row)

    if current_matrix:
        values_3d.append(np.array(current_matrix))

    values_3d = np.stack(values_3d)
    return np.array(z_nodes), values_3d


def _parse_z_value(line):
    return float(line.split('=')[1])


def _parse_data_row(line):
    parts = line.split()
    if len(parts) != 6:
        return None
    return [float(x) for x in parts[1:6]]