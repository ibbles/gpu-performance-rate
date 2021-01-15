# Motivation

Evaluating GPU performance improvements over time is difficult.
Changes in naming convention, new and different target customers, price fluctuations, inflation, new rendering techniques, and expanded feature sets and use cases make direct comparisons difficult.
Many comparisons in many different ways has been made, and this is an attempt to do it yet another way.
The intention is not to replace or even improve on all the other comparisons, it's only to complement them.

The main question for this text is, how fast are GPUs getting faster?


# Problem statement

The famous More's Law state that the number of transistors that cost-effectively can be put in a chip doubles every year, later revised to eighteen months.
Many take this to mean that the performance also doubles within the same about of time.
While that's debatable, there is no question that the real-world performance of microchips has seen a tremendous development over the decades since their introduction in the early '60s.
Exponential, in fact.
The purpose of this text is to explore that exponential growth within the context of GPUs, or Graphics Processing Units.

In short, what has the recent growth rate of GPU performance been?


# Method

This analysis assumes a steady exponential performance growth rate according to the standard exponential function

<img src="https://latex.codecogs.com/svg.latex?\fn_phv&space;f(t)&space;=&space;f(0)*e^{(k*t)}" title="f(t) = f(0)*e^{(k*t)}" />

where
- `f(t)` is the value of the function at time `t`.
- `f(0)` is the initial value of the function.
- `e` is Euler's number.
- `k` is the growth rate.
- `t` is amount of time during which the exponential growth is occurring.

Unfortunately for us, the GPU market is not a smooth performance curve with steady exponential growth, there is no well-defined `f(0)` here, and it's unclear what `t` should mean.
Instead we will take a pair-wise approach where the performance growth rate between two GPU with separate release dates is computed.
We use the following variant of the exponential function:

<img src="https://latex.codecogs.com/svg.latex?\fn_phv&space;p_{new}&space;=&space;p_{old}*e^{(k*t)}" title="p_{new} = p_{old}*e^{(k*t)}" />

where
- `p_new` is the performance of the newer of the two GPUs.
- `p_old` is the performance of the older of the two GPUs.
- `e` is still Euler's number.
- `k` is still the growth rate.
- `t` is the number of years between the two GPUs' release dates, as a real value rounded to months.

Of these the only thing that's unknown is `k`, which is exactly the growth rate that we've been discussing all along.
Let's solve for `k` so we can compute it from the data we already have.

-  `p_new = p_old*e^(k*t)`  Divide by `p_old`.
-  `p_new/p_old = e^(k*t)`  Take the natural logarithm of both sides.
-  `ln(p_new/p_old) = ln(e^(k*t)`  By definition, ln(e^x) = x.
-  `ln(p_new/p_old) = k*t`  Swap sides.
-  `k*t = ln(p_new/p_old)`  Divide by t.
-  `k = ln(p_new/p_old) / t`  Done!

<img src="https://latex.codecogs.com/svg.latex?\fn_phv&space;k&space;=&space;\frac{ln(\frac{p_{new}}{p_{old}})}{t}" title="k = \frac{ln(\frac{p_{new}}{p_{old}})}{t}" />

Next we need a definition for "performance", one that is applicable over the entire range of GPUs we are comparing.
I don't have access to all of this hardware myself so I'm relying on performance numbers from independent reviewers, in this case [sweclockers.com](https://www.sweclockers.com/artikel/18402-sweclockers-prestandaindex-for-grafikkort) using the numbers from the 3840x2160 tests.
A GPU's performance can't accurately be characterized by a single number, but let's work with what we have.

Using the performance numbers from the hardware reviewer we create the Cartesian product of the GPU list and feed each pair into the growth rate computation formula.


# Presentation

With a formula to compute the growth rate between two GPUs and a data set of GPUs to feed to the computation the next step is a way to present the results.

[gpus.svg](./gpus.svg) (best viewed in raw mode) is an image containing a grid or colored boxes.
The X axis, walking along columns in the grid, is a time line and each GPU in the data set is placed on that timeline.
The Y axis, walking down the rows of the grid, is a simple listing of the same GPUs in the same order.
The cells of the grid corresponds to a pair of GPUs, where the GPU on that row is the older GPU and the GPU on that column is the newer GPU.
Notice that the grid is roughly lower-triangular.
This is because we only compute growth rates from old-to-new GPUs, not from new-to-old, and the upper-left corner of the grid represents new-to-old pairs.
The columns on the right side of the grid contains many filled cells because those columns belong to the newest GPUs, and the newest GPUs has the highest number of older GPUs to compare against.

The filled cells are color coded based on the growth rate.
Green means that the newer GPU is faster than the old one, and red means that the newer GPU is slower.
A brighter color means a larger, in absolute value, growth rate so near black means almost no change in performance between the two GPUs.
Gray boxes indicate that the two GPUs was released on the same month, which is a singularity in the growth rate computation since the dates are at the month resolution.
Hovering the cursor over a filled cell reveal the names of the two GPUs, their respective performance numbers, the change in performance, the number of years between the two GPUs' release dates, and the computed growth rate.

The background color of the grid show whether the row belongs to an AMD GPU (red) or a Nvidia GPU (green).
Vertical lines does the same for the columns.


# Results

I encourage you to open the full-size version of the grid and follow along with the discussion below.
The grid cell pop-ups are useful to have.

![alt text](./gpus.svg "The full grid.")

A few observations.

GPUs are released in clusters, where several GPUs are released within a short time span.
This is expected for a series of GPUs, such as the 20 Super series from Nvidia, but we can see that the 20 Supers from Nvidia was released close to AMD's 5000 series, and Nvidias 30 series was released close to AMD's 6000 series.
This is where we find most of the gray cells, meaning that two GPUs were released on the same month.

![alt text](./images/20s_and_5000.png)


The brightest colors are for GPU pairs that released close to each other.
This is because in these cases product segmentation dominate over growth-over-time.
By that I mean that the slower GPU wasn't slower because it's lower on the technology ladder, but because the manufacturer deliberately placed it on a lower tier for cost, power usage, or size reasons.
In general, the grid cells at the top of the grid cell towers should probably be ignored.


![alt text](./images/30_and_6000.png)

The most interesting part, to me at least, is the lower-right corner of the grid.
This is where the most recent GPUs are compared against the oldest in the data set.
This is where we see the biggest effect of hardware development, where a very large difference in performance is spread over a large amount of time, so the growth rate should be a good indicator of the true average growth rate.

![alt text](./images/10_and_vega_and_2080_and_30_and_6000.png)

The colors themselves doesn't say all that much since it's mostly just green, except for the 2080 Ti row where we see that the GPU holds up well against the 3070 and the 6800.

![alt text](./images/lower_left_nums.png)
