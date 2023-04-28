from typing import Dict

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from utils import extract_durations


def plot_box_plots_per_run(ax: matplotlib.axes.Axes, data: Dict[int, np.ndarray]):
    ax.boxplot(data.values(), sym="", showmeans=True)
    ax.set_ylabel("duration in ms")

    if len(data.keys()) >= 8:
        tick_interval = 4

        for i, label in enumerate(ax.xaxis.get_ticklabels()):
            label.set_visible(i % tick_interval == 0)


def plot_boxes_in_subplot(data: [Dict[int, np.ndarray]], key: str):
    runs = len(data)
    assert runs % 2 == 0
    fig, axes = plt.subplots(int(runs / 2), 2)  # axes = [[11, 12], [21,22]]
    for i, ax in enumerate(axes):
        plot_box_plots_per_run(ax[0], data[i * 2])
        plot_box_plots_per_run(ax[1], data[i * 2 + 1])
    fig.suptitle("Durations of " + key)
    plt.show()


if __name__ == '__main__':
    routing_base_path = "../input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/routing/"
    non_routing_base_path = "../input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/no-routing/"

    key = "travel_time_collecting"
    plot_boxes_in_subplot([extract_durations(routing_base_path, 2 ** i, key) for i in range(1, 7)], key)
