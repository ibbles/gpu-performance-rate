#!/usr/bin/env python3

"""A program that computes the performance growth rate between pairs of GPUs.

Assumes exponential growth
  P(t) = P0 + e^(kt)
where
  P = Performance
  P0 = Some unknown/irrelevant base performance.
  k = Growth rate
  t = Time in months

The value computed and presented is k.

The output is an SVG images with a triangular grid of squares. Each row
represents an old GPU and each column repressents a new GPU. Each grid cell
represents a pair of GPUs and the cell is color coded by the performance growth
rate that increased the performance from the old card to the new card over the
number of months between the releases. Bright green means fast growth rate,
brigth red means fast negative growth rate, and black means near-zero growth
rate.

"""

import datetime

from types import SimpleNamespace
from functools import reduce


import svg_writer


class Annum:
    "A year and the grid column in which that year starts."
    def __init__(self, year):
        self.year = year
        self.column = None


class Gpu:
    def __init__(self, d):
        self.row = None
        self.column = None
        for key in d:
            setattr(self, key, d[key])


def dict_to_gpu(state):
    state.gpus = list(map(lambda d: Gpu(d), state.gpus))


def sort_gpus(state):
    state.gpus.sort(key=lambda gpu: gpu.date)


def find_date_range(state):
    state.start_date = datetime.date(state.gpus[0].date.year, 1, 1)
    state.end_date = datetime.date(state.gpus[-1].date.year, 12, 31)


def create_annum_dict(state):
    state.annums = {}
    for year in range(state.start_date.year, state.end_date.year + 1):
        state.annums[year] = Annum(year)


def num_months_between(old, new):
    """Return the number of month transitions between the two dates."""
    return (new.year - old.year) * 12 + (new.month - old.month)


def same_month(a, b):
    return a.year == b.year and a.month == b.month


def same_year(a, b):
    return a.year == b.year


def one_if_on_same_month(gpu_pair):
    return same_month(gpu_pair[0].date, gpu_pair[1].date) and 1 or 0


def num_month_collisions_in_year(state, year):
    gpus = list(filter(lambda gpu: gpu.date.year == year, state.gpus))
    return reduce(
        lambda num_collisions, pair:
            num_collisions + one_if_on_same_month(pair),
        zip(gpus[0:-1], gpus[1:]),
        0)


def assign_year_to_column(state):
    extra = 0
    for year in range(state.start_date.year, state.end_date.year + 1):
        annum = state.annums[year]
        annum.column = ((year - state.start_date.year) * 12) + extra
        extra += num_month_collisions_in_year(state, year)


def assign_gpu_to_column(state):
    gpus_by_year = {}
    for gpu in state.gpus:
        year_group = gpus_by_year.setdefault(gpu.date.year, [])
        year_group.append(gpu)

    for year in gpus_by_year:
        year_start = state.annums[year].column
        gpus = gpus_by_year[year]
        extra = 0
        last_month = 0
        for gpu in gpus:
            if gpu.date.month == last_month:
                extra += 1
            gpu.column = year_start + (gpu.date.month - 1) + extra
            last_month = gpu.date.month


def assign_gpu_to_row(state):
    for i, gpu in enumerate(state.gpus):
        gpu.row = len(state.gpus) - i


if __name__ == "__main__":
    import gpus
    state = SimpleNamespace()
    state.gpus = gpus.gpus
    dict_to_gpu(state)
    sort_gpus(state)
    find_date_range(state)
    create_annum_dict(state)
    assign_year_to_column(state)
    assign_gpu_to_column(state)
    assign_gpu_to_row(state)

    image = svg_writer.Image("gpus.svg")
    svg_writer.write_header(image)
    svg_writer.write_x_axis(state, image)
    svg_writer.write_y_axis(state, image)
    svg_writer.write_boxes(state, image)
    svg_writer.write_footer(image)
    print(f"{__name__} done.")
