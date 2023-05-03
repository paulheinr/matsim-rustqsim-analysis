import numpy as np
from matplotlib import pyplot as plt

from plotting.utils import extract_durations, BASE_PATH_ROUTING, get_mean_list

STACKED_TRAVEL_TIME_UPDATE_EVENTS = ["travel_time_collecting", "travel_time_aggregating", "travel_time_send",
                                     "travel_time_handling"]


def plot():
    max_power_of_runs = 6
    run_range = range(1, max_power_of_runs + 1)

    measured_data_by_key = {}
    for key in STACKED_TRAVEL_TIME_UPDATE_EVENTS:
        measured_data_by_key[key] = [extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in run_range]

    means_by_key = {k: get_mean_list(v) for k, v in measured_data_by_key.items()}

    fig, ax = plt.subplots()
    bottom = np.zeros(max_power_of_runs)

    for key, means in means_by_key.items():
        bar = ax.bar([str(2 ** i) for i in run_range], means, 0.5, label=key, bottom=bottom)
        ax.bar_label(bar, label_type="center")
        bottom += np.array(means)

    ax.set_title("Duration of Phases During Travel Time Updating")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), title="Phases", loc='upper right')

    ax.grid(True, axis="y")
    ax.set_xlabel("# MPI-Slots")
    ax.set_xlabel("Duration in ms")
    plt.show()


if __name__ == "__main__":
    plot()
