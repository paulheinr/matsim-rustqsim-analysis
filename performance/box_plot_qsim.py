from typing import Dict

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import double

import utils


def get_trace_file_path(base_path, mpi_slots, slot) -> str:
    return base_path + "/trace" + str(mpi_slots) + "/mpi_qsim_" + str(slot)


def extract_sim_durations(base_path: str) -> Dict[int, np.ndarray]:
    sim_durations_by_mpi_slots = {}
    max_power = 7
    for mpi_slots in (2 ** p for p in range(0, max_power)):
        sim_durations_fixed_slot_amount = []

        for i in range(0, mpi_slots):
            events = utils.load_json_event(get_trace_file_path(base_path, mpi_slots, i))
            data = get_duration(events, "simulation")
            assert data.size == 1
            sim_durations_fixed_slot_amount.append(data[0])

        sim_durations_by_mpi_slots[mpi_slots] = np.array(sim_durations_fixed_slot_amount)

    return sim_durations_by_mpi_slots


def extract_qsim_comm_durations(base_path: str, mpi_slots: int) -> Dict[int, pd.DataFrame]:
    result = {}
    for i in range(0, mpi_slots):
        events = utils.load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        duration_qsim_step = get_duration(events, "qsim_step")
        duration_mpi_send = get_duration(events, "mpi_send")
        duration_mpi_recv = get_duration(events, "mpi_receive")
        result[i] = pd.DataFrame(
            {"qsim_step": duration_qsim_step, "mpi_send": duration_mpi_send,
             "mpi_receive": duration_mpi_recv})
        print("\n------ SLOT # " + str(i) + " ------")
        print("\n## QSim Step ##")
        print(pd.DataFrame(duration_qsim_step).describe())
        print("\n## MPI Send ##")
        print(pd.DataFrame(duration_mpi_send).describe())
        print("\n## MPI Receive ##")
        print(pd.DataFrame(duration_mpi_recv).describe())
    return result


def get_duration(events, key) -> np.ndarray:
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return np.array(list(map(lambda e: utils.duration_in_milliseconds(e["duration"]), filtered_events)))


def get_speedup_by_slots(durations: Dict[int, np.ndarray]) -> tuple[np.ndarray[int], np.ndarray[double]]:
    base_duration = np.average(durations[1])
    return np.array([k for k in durations.keys()]), np.array(
        [base_duration / np.average(e) for e in durations.values()])


# plots boxplot of simulation durations
# x: # MPI slots
# y: duration in ms
def plot_box_plot_sim_duration(sim_durations: Dict[int, np.ndarray]):
    fig, ax = plt.subplots()
    ax.boxplot(sim_durations.values())
    ax.set_xticklabels(sim_durations.keys())
    ax.set_yscale("log")


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
    routing_base_path = "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/routing/"
    non_routing_base_path = "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/no-routing/"

    routing_durations: Dict[int, np.ndarray] = extract_sim_durations(routing_base_path)
    no_routing_durations: Dict[int, np.ndarray] = extract_sim_durations(non_routing_base_path)

    # box_plot_sim_duration(durations)

    # plot_speedup_both(routing_durations, no_routing_durations)

    plot_qsim_comm_subplots([extract_qsim_comm_durations(non_routing_base_path, 2 ** i) for i in range(1, 7)])
