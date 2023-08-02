from math import ceil

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from plotting.utils import GENERAL_EVENTS, extract_durations, BASE_PATH_NON_ROUTING, ROUTING_EVENTS, BASE_PATH_ROUTING, \
    get_speedup_list


def plot_speedup_per_key(ax: matplotlib.axes.Axes, key, data: [[np.ndarray]]):
    number_of_slots_in_base_run = len(data[0]) - 1
    speedups = get_speedup_list(data)
    x_ticks = [2 ** i for i in range(number_of_slots_in_base_run, len(speedups) + number_of_slots_in_base_run)]

    ax.plot(x_ticks, speedups, "x-")
    # ax.set_xscale("log")
    # ax.set_xticks(x_ticks)
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.minorticks_off()

    ax.set_title("Speed up " + key)
    ax.grid(True)
    ax.set_ylabel("speedup factor")
    ax.set_xlabel("# MPI slots")


def plot_speedup_in_subplot(speedup_by_key, scenario):
    rows = ceil(len(speedup_by_key) / 2)
    fig, axes = plt.subplots(rows, 2)  # axes = [[11, 12], [21,22]]
    for i, (key, data) in enumerate(speedup_by_key.items()):
        row = int(i / 2)
        column = i % 2
        plot_speedup_per_key(axes[row, column], key, data)
    fig.suptitle("Scenario: " + scenario)
    pass


def get_speedup_base_line(key):
    return 1 if "send" in key or "receive" in key else 0


def plot_for_non_routing():
    speedup_by_key = {}
    for key in GENERAL_EVENTS:
        speedup_by_key[key] = [extract_durations(BASE_PATH_NON_ROUTING, 2 ** i, key) for i in
                               range(get_speedup_base_line(key), 7)]

    plot_speedup_in_subplot(speedup_by_key, "Non-Routing")
    plt.show()


def plot_for_routing():
    speedup_by_key = {}
    for key in GENERAL_EVENTS + ROUTING_EVENTS:
        speedup_by_key[key] = [extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in
                               range(get_speedup_base_line(key), 7)]

    plot_speedup_in_subplot(speedup_by_key, "Routing")
    plt.show()


if __name__ == "__main__":
    plot_for_routing()
