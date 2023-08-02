import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from utils import extract_durations, BASE_PATH_ROUTING, BASE_PATH_NON_ROUTING, GENERAL_EVENTS, ROUTING_EVENTS


def plot_box_plots_per_run(ax: matplotlib.axes.Axes, data: [np.ndarray]):
    ax.boxplot(data, sym="", showmeans=True)
    ax.set_ylabel("Duration in ms")
    ax.set_xlabel("Process")

    if len(data) >= 8:
        tick_interval = 4

        for i, label in enumerate(ax.xaxis.get_ticklabels()):
            label.set_visible(i % tick_interval == 0)


def plot_boxes_in_subplot(data: [[np.ndarray]], key: str):
    runs = len(data)
    assert runs % 2 == 0
    fig, axes = plt.subplots(int(runs / 2), 2, figsize=(10, 15))  # axes = [[11, 12], [21,22]]
    for i, ax in enumerate(axes):
        plot_box_plots_per_run(ax[0], data[i * 2])
        plot_box_plots_per_run(ax[1], data[i * 2 + 1])
    # fig.suptitle("Durations of " + get_display_value_for_key(key))
    fig.savefig("box_plots_" + key + ".pdf")


def plot_for_routing():
    for key in ROUTING_EVENTS:
        plot_boxes_in_subplot([extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in range(1, 7)], key)


def plot_for_non_routing():
    for key in GENERAL_EVENTS:
        plot_boxes_in_subplot([extract_durations(BASE_PATH_NON_ROUTING, 2 ** i, key) for i in range(1, 7)], key)


def plot_for_query():
    for key in ["qsim"]:
        plot_boxes_in_subplot([extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in range(1, 7)], key)


if __name__ == '__main__':
    plot_for_query()
    plt.show()
