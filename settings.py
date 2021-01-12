from math import isnan
from types import SimpleNamespace
from typing import List


def mix(f, a, b):
    return (1-f)*a + f*b


def mix_colors(f, a, b):
    return [mix(f, c1, c2) for c1, c2 in zip(a, b)]


def pick_color(value: float, color: List[int]):
    progress = min(value, 100) / 100.0
    f = progress**0.4
    return mix_colors(f, [0.0, 0.0, 0.0], color)


def color_range(value: float):
    if isnan(value):
        return [127] * 3
    if value >= 0:
        return pick_color(value, [0, 255, 0])
    else:
        return pick_color(-value, [255, 0, 0])


def make_settings():
    settings = dict(
        scale=1,
        row_height=30,
        column_width=30,
        timeline_gap=120,
        grid_top_gap=150,
        left_gap=100,
        color_range=color_range)

    return SimpleNamespace(**settings)


settings = make_settings()
