from typing import Dict

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from numpy import double

import utils


def extract_sim_durations(base_path: str) -> Dict[int, np.ndarray]:
    sim_durations_by_mpi_slots = {}
    max_power = 7
    for mpi_slots in (2 ** p for p in range(0, max_power)):
        sim_durations_fixed_slot_amount = []

        for i in range(0, mpi_slots):
            events = utils.load_json_event(base_path + "/trace" + str(mpi_slots) + "/mpi_qsim_" + str(i))
            data = get_duration(events, "simulation")
            assert data.size == 1
            sim_durations_fixed_slot_amount.append(data[0])

        sim_durations_by_mpi_slots[mpi_slots] = np.array(sim_durations_fixed_slot_amount)

    return sim_durations_by_mpi_slots


def get_duration(events, key) -> np.ndarray:
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return np.array(list(map(lambda e: utils.duration_in_milliseconds(e["duration"]), filtered_events)))


def get_speedup_by_slots(durations: Dict[int, np.ndarray]) -> tuple[np.ndarray[int], np.ndarray[double]]:
    base_duration = np.average(durations[1])
    return np.array([k for k in durations.keys()]), np.array(
        [base_duration / np.average(e) for e in durations.values()])


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


def plot_speedup_both(routing_durations: Dict[int, np.ndarray], no_routing_durations: Dict[int, np.ndarray]):
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(10, 5))
    plot_speedup(ax1, get_speedup_by_slots(routing_durations), "speedup for routing")
    plot_speedup(ax2, get_speedup_by_slots(no_routing_durations), "speedup for non routing")

    plt.show()


if __name__ == '__main__':
    routing_durations: Dict[int, np.ndarray] = extract_sim_durations(
        "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/routing/")
    no_routing_durations: Dict[int, np.ndarray] = extract_sim_durations(
        "./input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/no-routing/")
    # box_plot_sim_duration(durations)

    plot_speedup_both(routing_durations, no_routing_durations)
