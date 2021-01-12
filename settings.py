from types import SimpleNamespace
from typing import List


def pick_color_interval(value: float, stops: List[SimpleNamespace]):
    for lower, upper in zip(stops[:-1], stops[1:]):
        if value >= lower.value and value < upper.value:
            return SimpleNamespace(lower=lower, upper=upper)

    invalid = SimpleNamespace(value=value, color=[110, 110, 110])
    return SimpleNamespace(lower=invalid, upper=invalid)


def mix(f, a, b):
    return (1-f)*a + f*b


def mix_colors(f, a, b):
    return [mix(f, c1, c2) for c1, c2 in zip(a, b)]


def pick_color(value: float, colors: List[List[int]]):
    interval = pick_color_interval(value, colors)
    width = interval.upper.value - interval.lower.value
    if width > 0.0:
        progress = (value - interval.lower.value) / width
    else:
        progress = 0.0
    return mix_colors(progress, interval.lower.color, interval.upper.color)


def color_range(value: float):
    positive_stops = [
        SimpleNamespace(value=0, color=[0, 0, 0]),
        SimpleNamespace(value=20, color=[0, 125, 8]),
        SimpleNamespace(value=100, color=[187, 91, 201]),
        SimpleNamespace(value=300, color=[0, 255, 0])
    ]

    negative_stops = [
        SimpleNamespace(value=0, color=[0, 0, 0]),
        SimpleNamespace(value=20, color=[26, 185, 217]),
        SimpleNamespace(value=100, color=[255, 111, 28]),
        SimpleNamespace(value=300, color=[255, 0, 0])
    ]

    if value >= 0:
        return pick_color(value, positive_stops)
    else:
        return pick_color(-value, negative_stops)


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
