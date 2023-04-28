from typing import Dict

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from numpy import double

from utils import extract_sim_durations


def get_speedup_by_slots(durations: Dict[int, np.ndarray]) -> tuple[np.ndarray[int], np.ndarray[double]]:
    base_duration = np.average(durations[1])
    return np.array([k for k in durations.keys()]), np.array(
        [base_duration / np.average(e) for e in durations.values()])


def plot_speedup(ax: matplotlib.axes.Axes, averages_by_slots: tuple[np.ndarray[int], np.ndarray[double]], title: str):
    ax.plot(averages_by_slots[0], averages_by_slots[1], ".-")
    ax.set_xscale("log")
    ax.set_title(title)
    x_ticks = [2 ** i for i in range(0, averages_by_slots[1].size)]
    ax.set_xticks(x_ticks)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.minorticks_off()
    ax.grid(True)
    ax.set_ylabel("speedup factor")
    ax.set_xlabel("# MPI slots")


# plots speedup graph for both routing and non-routing scenario
# x: # MPI slots
# y: speedup factor
def plot_speedup_both(routing_durations: Dict[int, np.ndarray], no_routing_durations: Dict[int, np.ndarray]):
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(10, 5))
    plot_speedup(ax1, get_speedup_by_slots(routing_durations), "Speedup for Routing")
    plot_speedup(ax2, get_speedup_by_slots(no_routing_durations), "Speedup for Non-Routing")

    plt.show()


if __name__ == '__main__':
    routing_base_path = "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/routing/"
    non_routing_base_path = "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/no-routing/"

    routing_durations: Dict[int, np.ndarray] = extract_sim_durations(routing_base_path)
    no_routing_durations: Dict[int, np.ndarray] = extract_sim_durations(non_routing_base_path)

    plot_speedup_both(routing_durations, no_routing_durations)
