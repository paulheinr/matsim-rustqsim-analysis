import numpy as np
from matplotlib import pyplot as plt

import plotting.utils as utils
from plotting.utils import extract_durations_interval, get_mean_list, get_display_value_for_key

STACKED_TRAVEL_TIME_UPDATE_EVENTS = ["travel_time_aggregating", "travel_time_augmenting", "travel_time_communicating",
                                     "travel_time_handling"]


def plot():
    number_of_runs = 4
    run_range = range(0, number_of_runs)

    measured_data_by_key = {}
    for key in STACKED_TRAVEL_TIME_UPDATE_EVENTS:
        measured_data_by_key[key] = [extract_durations_interval("../" + utils.BASE_PATH_INTERVAL, i, key) for i in
                                     utils.INTERVALS]

    means_by_key = {k: get_mean_list(v) for k, v in measured_data_by_key.items()}

    fig, ax = plt.subplots()
    bottom = np.zeros(number_of_runs)

    print("--- RESULTS ---")
    print("Aggregate, Extend, Communicate, Handle, Sum")
    for key, means in means_by_key.items():
        bar = ax.bar([str(i) for i in utils.INTERVALS], means, 0.6, label=key, bottom=bottom)
        # if key in ["travel_time_augmenting"]:
        ax.bar_label(bar, label_type="center")
        print(np.around(means, 2))
        bottom += np.array(means)

    print(np.around(bottom, 2))

    # ax.set_title("Duration of Phases During Travel Time Updating")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed([get_display_value_for_key(l) for l in labels]), title="Phases",
              loc='center right')

    ax.grid(True, axis="y", alpha=0.3)

    ax.set_xlabel("Interval")
    ax.set_ylabel("Duration in ms")
    plt.show()


if __name__ == "__main__":
    plot()
