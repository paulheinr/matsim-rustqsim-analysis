from matplotlib import pyplot as plt

from plotting.utils import GENERAL_EVENTS, extract_durations, BASE_PATH_NON_ROUTING, BASE_PATH_ROUTING, \
    get_speedup_list


def plot_speedup(speedup_by_key):
    speedups_aggregation = get_speedup_list(speedup_by_key.get("travel_time_aggregating"))
    speedups_extension = get_speedup_list(speedup_by_key.get("travel_time_augmenting"))
    x_ticks = [2 ** i for i in range(0, 8)]
    # x_ticks = [2 ** i for i in range(number_of_slots_in_base_run, len(speedups) + number_of_slots_in_base_run)]

    # plt.plot(x_ticks, speedups, "x-")
    # ax.set_xscale("log")
    # ax.set_xticks(x_ticks)
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.minorticks_off()

    fig, ax = plt.subplots()
    ax.plot(x_ticks, speedups_aggregation, label="Aggregation", linestyle=":", marker=".")
    ax.plot(x_ticks, speedups_extension, label="Extension", linestyle=":", marker="^")

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)

    # ax.set_title("Speed-up of Aggregation and Extension")
    ax.grid(True)
    ax.set_ylabel("Speed-up Factor")
    ax.set_xlabel("# Processes")

    ax.get_xaxis().set_major_formatter('{x:.0f}')
    ax.get_yaxis().set_major_formatter('{x:.0f}')

    ax.legend()


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
        speedup_by_key[key] = [extract_durations(BASE_PATH_ROUTING, 2 ** i, key) for i in
                               range(get_speedup_base_line(key), 8)]

    plot_speedup(speedup_by_key)
    plt.show()


if __name__ == "__main__":
    plot_for_routing()
