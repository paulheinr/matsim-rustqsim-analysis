from typing import Dict

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import extract_sim_durations, BASE_PATH_ROUTING, BASE_PATH_NON_ROUTING


def get_trace_file_path(base_path, mpi_slots, slot) -> str:
    return base_path + "/trace" + str(mpi_slots) + "/mpi_qsim_" + str(slot)


# plots boxplot of simulation durations
# x: # MPI slots
# y: duration in ms
def plot_box_plot_sim_duration(sim_durations: Dict[int, np.ndarray]):
    fig, ax = plt.subplots()
    ax.boxplot(sim_durations.values())
    ax.set_xticklabels(sim_durations.keys())
    ax.set_yscale("log")

    plt.show()


# example: https://rowannicholls.github.io/python/graphs/plt_based/boxplots_multiple_groups.html
# x: qsim_step, mpi_send, mpi_receive
# y: duration
def plot_qsim_comm_box_plots(ax: matplotlib.axes.Axes, data: Dict[int, pd.DataFrame]):
    # Set x-positions for boxes
    number_of_slots = len(data.keys())
    box_plots_per_slot = 3

    x_pos_range = np.arange(number_of_slots) / (number_of_slots - 1)
    x_pos = (x_pos_range * 0.5) + 0.75

    # Plot
    for mpi_slots, duration_arrays in data.items():
        bp = ax.boxplot(
            np.array(duration_arrays), sym='', whis=[0, 100], widths=0.4 / number_of_slots,
            labels=list(duration_arrays),
            positions=[x_pos[mpi_slots] + j * 1 for j in range(len(duration_arrays.T))]
        )

    # Titles
    ax.set_title("Durations of simulation with " + str(number_of_slots) + " slots")
    ax.set_ylabel("duration in ms")

    # Axis ticks and labels
    ax.set_xticks(np.arange(box_plots_per_slot) + 1)
    ax.xaxis.set_minor_locator(matplotlib.ticker.FixedLocator(
        np.array(range(box_plots_per_slot + 1)) + 0.5)
    )
    ax.tick_params(axis='x', which='minor', length=3)
    ax.tick_params(axis='x', which='major', length=0)
    # Change the limits of the x-axis
    ax.set_xlim([0.5, box_plots_per_slot + 0.5])

    plt.gca()


def plot_qsim_comm_subplots(data: [Dict[int, pd.DataFrame]]):
    runs = len(data)
    assert runs % 2 == 0
    fig, axes = plt.subplots(int(runs / 2), 2)  # axes = [[11, 12], [21,22]]
    for i, ax in enumerate(axes):
        plot_qsim_comm_box_plots(ax[0], data[i * 2])
        plot_qsim_comm_box_plots(ax[1], data[i * 2 + 1])
    plt.show()


if __name__ == '__main__':
    routing_durations: Dict[int, np.ndarray] = extract_sim_durations(BASE_PATH_ROUTING, 7)
    no_routing_durations: Dict[int, np.ndarray] = extract_sim_durations(BASE_PATH_NON_ROUTING, 7)

    plot_box_plot_sim_duration(routing_durations)
