#!/usr/bin/env python3

"""A program that computes the performance growth rate between pairs of GPUs.

Assumes exponential growth
  p = a*e^(k*t)
where
  p = Current performance.
  a = Performance at time 0.
  k = Growth rate.
  t = Current time.

For each GPU we know its performance and release date, so p, a, and t are known.
  p = Performance of new GPU.
  a = Performance of old GPU.
  t = Time in years between the GPUs' release date.

The value computed and presented is k. It is computed as

      log(p/a)
  k = ---------
         t

This equation was derived as follows:

  p = a*e^(k*t) ; Divide by a.
  p/a = e^(k*t) ; Take the natural logarithm of both sides.
  ln(p/a) = ln(e^(k*t) ; By definition, ln(e^x) = x.
  ln(p/a) = k*t ; Swap sides.
  k*t = ln(p/a) ; Divide by t.
  k = ln(p/a) / t ; Done!


The output of this program is an SVG images with a triangular grid of
squares. Each row represents an old GPU and each column repressents a new
GPU. Each grid cell represents a pair of GPUs and the cell is color coded based
on the performance growth rate that increased the performance from the old card
to the new card over the number of years between the releases. Bright green
means fast growth rate, brigth red means fast negative growth rate, and black
means near-zero growth rate.

Hovering over a cell displayes a pop-up that names the two GPU and shows the
time between their respective releases as well as the computed growth rate.

There is a time line along the top of the image that shows when each GPU was
released. There is one column per month unless multiple GPUs were release on the
same month. In that case the month is as many grid columns wide as there were
GPUs released that month.
"""

from types import SimpleNamespace
from functools import reduce


import gpus
import svg_writer


class Annum:
    """A year and the grid column in which that year starts, accounding for prior
    multi-column months.
    """
    def __init__(self, year):
        self.year = year
        self.column = None


class Gpu:
    """Data about a single GPU.
    Initialized from of of the entries in gpus.py.
    """
    def __init__(self, d):
        self.row = None
        self.column = None
        for key in d:
            setattr(self, key, d[key])


def dict_to_gpu(state):
    """Convert the input GPU data dictionaries, read from gpu.py, into Gpu
    instances.
    """
    state.gpus = list(map(lambda d: Gpu(d), state.gpus))


def sort_gpus(state):
    """Sort the GPU data by release date."""
    state.gpus.sort(key=lambda gpu: gpu.date)


def find_date_range(state):
    """Find the range of years that cover all the GPU releases."""
    state.start_year = state.gpus[0].date.year
    state.end_year = state.gpus[-1].date.year
    state.years = range(state.start_year, state.end_year + 1)


def create_annum_dict(state):
    """Create a dictionary with one Annum instance per year in the date range.
    """
    state.annums = {year: Annum(year) for year in state.years}


def num_months_between(old, new):
    """Return the number of month transitions between the two dates.
    The number of transitions, so there is one month between January 31 and
    February 1.
    """
    return (new.year - old.year) * 12 + (new.month - old.month)


def same_month(a, b):
    return a.year == b.year and a.month == b.month


def same_year(a, b):
    return a.year == b.year


def one_if_on_same_month(gpu_pair):
    return same_month(gpu_pair[0].date, gpu_pair[1].date) and 1 or 0


def num_month_collisions_in_year(state, year):
    """Count the number of consecutive pair GPUs that released in the same
    month of the given year. This is the same as the number of extra grid
    columns that year has.
    """
    gpus = list(filter(lambda gpu: gpu.date.year == year, state.gpus))
    return reduce(
        lambda num_collisions, pair:
            num_collisions + one_if_on_same_month(pair),
        zip(gpus[0:-1], gpus[1:]),
        0)


def assign_year_to_column(state):
    """Find which grid column corresponds to each year's January."""
    extra = 0  # The number of extra colums due to release collisions so far.
    for year in state.years:
        annum = state.annums[year]
        months_to_january = (year - state.start_year) * 12
        annum.column = months_to_january + extra
        extra += num_month_collisions_in_year(state, year)


def assign_gpu_to_column(state):
    """Assign each GPU to its own grid column.
    We know that all GPUs will with within their own year since we padded years
    with collisions with extra columns.
    """
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
            # -1 because January is 1, but we want January to start 0 columns
            # after the year start column.
            gpu.column = year_start + (gpu.date.month - 1) + extra
            last_month = gpu.date.month


def assign_gpu_to_row(state):
    """ Give each GPU its own row.
    We don't do the month stuff for rows, just pack them one after the other.
    """
    for i, gpu in enumerate(state.gpus):
        gpu.row = len(state.gpus) - i


if __name__ == "__main__":
    state = SimpleNamespace()
    state.gpus = gpus.gpus
    dict_to_gpu(state)
    sort_gpus(state)
    find_date_range(state)
    create_annum_dict(state)
    assign_year_to_column(state)
    assign_gpu_to_column(state)
    assign_gpu_to_row(state)

    svg_writer.write_image(state, "gpus.svg")
    print(f"{__name__} done.")
