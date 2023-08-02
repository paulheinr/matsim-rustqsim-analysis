import numpy as np
from matplotlib import pyplot as plt

from plotting.utils import extract_durations, BASE_PATH_ROUTING, get_mean_list, get_display_value_for_key

STACKED_TRAVEL_TIME_UPDATE_EVENTS = ["travel_time_aggregating", "travel_time_augmenting", "travel_time_communicating",
                                     "travel_time_handling"]


def plot():
    max_power_of_runs = 10
    run_range = range(0, max_power_of_runs + 1)

    measured_data_by_key = {}
    for key in STACKED_TRAVEL_TIME_UPDATE_EVENTS:
        measured_data_by_key[key] = [extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in run_range]

    means_by_key = {k: get_mean_list(v) for k, v in measured_data_by_key.items()}

    fig, ax = plt.subplots()
    bottom = np.zeros(max_power_of_runs + 1)

    print("--- RESULTS ---")
    print("Aggregate, Extend, Communicate, Handle, Sum")
    for key, means in means_by_key.items():
        bar = ax.bar([str(2 ** i) for i in run_range], means, 0.6, label=key, bottom=bottom)
        # if key in ["travel_time_augmenting"]:
        ax.bar_label(bar, label_type="center")
        print(np.around(means, 2))
        bottom += np.array(means)

    print(np.around(bottom, 2))

    # ax.set_title("Duration of Phases During Travel Time Updating")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed([get_display_value_for_key(l) for l in labels]), title="Phases",
              loc='upper right')

    ax.grid(True, axis="y", alpha=0.3)

    ax.set_xlabel("# Processes")
    ax.set_ylabel("Duration in ms")
    plt.show()


if __name__ == "__main__":
    plot()
