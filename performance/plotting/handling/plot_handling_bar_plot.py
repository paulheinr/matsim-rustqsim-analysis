import numpy as np
from matplotlib import pyplot as plt

from plotting.utils import extract_durations, BASE_PATH_ROUTING, get_mean_list, get_display_value_for_key

STACKED_TRAVEL_TIME_HANDLING_EVENTS = ["travel_time_handling_fold", "travel_time_handling_clone",
                                       "router_customization"]


def plot():
    max_power_of_runs = 10
    run_range = range(0, max_power_of_runs + 1)

    measured_data_by_key = {}
    for key in STACKED_TRAVEL_TIME_HANDLING_EVENTS:
        measured_data_by_key[key] = [extract_durations("../" + BASE_PATH_ROUTING, 2 ** i, key) for i in run_range]

    means_by_key = {k: get_mean_list(v) for k, v in measured_data_by_key.items()}

    fig, ax = plt.subplots()
    bottom = np.zeros(max_power_of_runs + 1)

    for key, means in means_by_key.items():
        bar = ax.bar([str(2 ** i) for i in run_range], means, 0.6, label=key, bottom=bottom)
        # if key in ["travel_time_augmenting"]:
        # ax.bar_label(bar, label_type="center")
        bottom += np.array(means)

    # ax.set_title("Duration of Phases During Travel Time Updating")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed([get_display_value_for_key(l) for l in labels]), title="Steps",
              loc="lower left")

    ax.grid(True, axis="y", alpha=0.3)

    ax.set_xlabel("# Processes")
    ax.set_ylabel("Duration in ms")
    plt.show()


if __name__ == "__main__":
    plot()
