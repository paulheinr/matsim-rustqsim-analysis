import numpy as np
from matplotlib import pyplot as plt

from plotting.utils import GENERAL_EVENTS, extract_durations, BASE_PATH_NON_ROUTING, BASE_PATH_ROUTING, \
    get_speedup_list, get_display_value_for_key


def plot_speedup(speedup_by_key):
    speedups_aggregation = get_speedup_list(speedup_by_key.get("travel_time_aggregating"))
    speedups_extension = get_speedup_list(speedup_by_key.get("travel_time_augmenting"))
    x_ticks = [2 ** i for i in range(0, 11)]
    # x_ticks = [2 ** i for i in range(number_of_slots_in_base_run, len(speedups) + number_of_slots_in_base_run)]

    # plt.plot(x_ticks, speedups, "x-")
    # ax.set_xscale("log")
    # ax.set_xticks(x_ticks)
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.minorticks_off()

    fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 1]})
    ax[0].plot(x_ticks, speedups_aggregation, label=get_display_value_for_key("travel_time_aggregating"), linestyle=":",
               marker=".")
    ax[1].plot(x_ticks, speedups_extension, label=get_display_value_for_key("travel_time_augmenting"), linestyle=":",
               marker=".")

    for i in [0, 1]:
        ax[i].set_xscale("log", base=2)
        ax[i].set_yscale("log", base=2)

        ax[i].set_xlim([0, 1200])
        ax[i].set_ylim([0, 1200])

        ax[i].set_xticks(np.logspace(0, 10, num=11, base=2))
        ax[i].set_yticks(np.logspace(0, 10, num=11, base=2))

        # ax.set_title("Speed-up of Aggregation and Extension")
        ax[i].grid(True)
        ax[i].set_ylabel("Speed-up Factor")
        ax[i].set_xlabel("# Processes")

        ax[i].get_xaxis().set_major_formatter('{x:.0f}')
        ax[i].get_yaxis().set_major_formatter('{x:.0f}')

        ax[i].legend()


def get_speedup_base_line(key):
    return 1 if "send" in key or "receive" in key else 0


def plot_for_non_routing():
    speedup_by_key = {}
    for key in GENERAL_EVENTS:
        speedup_by_key[key] = [extract_durations(BASE_PATH_NON_ROUTING, 2 ** i, key) for i in
                               range(get_speedup_base_line(key), 7)]

    plot_speedup(speedup_by_key, "Non-Routing")
    plt.show()


def plot_for_routing():
    speedup_by_key = {}
    for key in ["travel_time_aggregating", "travel_time_augmenting"]:
        speedup_by_key[key] = [extract_durations("../" + BASE_PATH_ROUTING, 2 ** i, key) for i in
                               range(get_speedup_base_line(key), 11)]

    plot_speedup(speedup_by_key)
    plt.show()


if __name__ == "__main__":
    plot_for_routing()
