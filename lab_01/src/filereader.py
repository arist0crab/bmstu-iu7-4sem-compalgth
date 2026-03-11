import numpy as np


def load_all_data(filepath):
    with open(filepath, 'r', encoding='windows-1251') as f:
        lines = f.readlines()

    idx = 0
    data = {}

    while idx < len(lines):
        line = lines[idx].strip()

        if 'R=0.25' in line or 'ток' in line.lower():
            current_data, idx = _parse_current_table(lines, idx)
            data['current'] = current_data

        elif 'Nh' in line or 'концентрац' in line.lower():
            nh_data, idx = _parse_2d_table(lines, idx)
            data['nh'] = nh_data

        elif 'электропровод' in line.lower() or 'sigma' in line.lower():
            sigma_data, idx = _parse_2d_table(lines, idx)
            data['sigma'] = sigma_data

        elif 'теплоемк' in line.lower() or 'С(T,p)' in line:
            c_data, idx = _parse_2d_table(lines, idx)
            data['c'] = c_data

        elif 'мощность' in line.lower() or 'q(T,p)' in line:
            q_data, idx = _parse_2d_table(lines, idx)
            data['q'] = q_data

        else:
            idx += 1

    return data


def _parse_current_table(lines, start_idx):
    time = []
    current = []

    idx = start_idx + 1
    while idx < len(lines) and '№' not in lines[idx]:
        idx += 1
    idx += 1

    while idx < len(lines):
        line = lines[idx].strip()
        if _is_new_table_section(line):
            break

        parts = line.split()
        if len(parts) >= 3:
            t_str = _normalize_number(parts[1])
            i_str = _normalize_number(parts[2])

            if _is_float(t_str) and _is_float(i_str):
                time.append(float(t_str))
                current.append(float(i_str))
        idx += 1

    return {
        'time': np.array(time),
        'current': np.array(current)
    }, idx


def _parse_2d_table(lines, start_idx):
    idx = start_idx + 1
    pressures = _extract_pressures(lines, idx)
    idx = _advance_to_first_data_row(lines, idx)

    temperatures = []
    values = []

    while idx < len(lines):
        line = lines[idx].strip()
        if _should_skip_line(line):
            idx += 1
            continue

        if _is_new_table_section(line):
            break

        parts = line.split()
        if len(parts) >= 4:
            temp_str = _normalize_number(parts[0])
            if _is_float(temp_str):
                temperatures.append(float(temp_str))
                row = _parse_row_values(parts[1:4])
                values.append(row)
        idx += 1

    return {
        'temperatures': np.array(temperatures),
        'pressures': pressures,
        'values': np.array(values)
    }, idx


def _extract_pressures(lines, start_idx):
    default = np.array([0.5, 1.5, 2.5])
    idx = start_idx

    while idx < len(lines):
        line = lines[idx].strip()
        if 'МПа' in line or 'ат' in line:
            numbers = []
            for part in line.split():
                cleaned = part.replace('МПа', '').replace('ат', '').strip()
                normalized = _normalize_number(cleaned)
                if cleaned and _is_float(normalized):
                    numbers.append(float(normalized))
            if len(numbers) >= 3:
                return np.array(numbers[:3])
        idx += 1

    return default


def _advance_to_first_data_row(lines, start_idx):
    idx = start_idx
    while idx < len(lines):
        line = lines[idx].strip()
        if line and not _should_skip_line(line) and not _is_new_table_section(line):
            parts = line.split()
            if len(parts) >= 4 and _is_float(_normalize_number(parts[0])):
                break
        idx += 1
    return idx


def _parse_row_values(parts):
    values = []
    for part in parts:
        values.append(_parse_number(part))

    while len(values) < 3:
        values.append(0.0)

    return values[:3]


def _is_new_table_section(line):
    keywords = ['концентрац', 'электро', 'тепло', 'мощность', 'ток']
    return any(key in line.lower() for key in keywords)


def _should_skip_line(line):
    return not line or '-----' in line


def _normalize_number(s):
    return s.replace(',', '.').strip()


def _is_float(s):
    if not s:
        return False

    s = s.strip()
    if not s:
        return False

    if 'e' in s.lower():
        parts = s.lower().split('e')
        if len(parts) != 2:
            return False
        return _is_simple_float(parts[0]) and _is_integer(parts[1])

    return _is_simple_float(s)


def _is_simple_float(s):
    if not s:
        return False

    s = s.strip()
    if not s:
        return False

    if s[0] in '+-':
        s = s[1:]

    if not s:
        return False

    dot_count = 0
    for char in s:
        if char == '.':
            dot_count += 1
            if dot_count > 1:
                return False
        elif not char.isdigit():
            return False

    return True


def _is_integer(s):
    if not s:
        return False

    s = s.strip()
    if not s:
        return False

    if s[0] in '+-':
        s = s[1:]

    if not s:
        return False

    return all(char.isdigit() for char in s)


def _parse_number(s):
    s = _normalize_number(s)
    return float(s) if _is_float(s) else 0.0
