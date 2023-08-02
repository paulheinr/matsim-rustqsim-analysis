from matplotlib import pyplot as plt

from plotting.utils import extract_durations, BASE_PATH_ROUTING, \
    get_speedup_list


def plot_speedup(data):
    speedups = get_speedup_list(data)
    x_ticks = [2 ** i for i in range(0, len(data))]
    # x_ticks = [2 ** i for i in range(number_of_slots_in_base_run, len(speedups) + number_of_slots_in_base_run)]

    # plt.plot(x_ticks, speedups, "x-")
    # ax.set_xscale("log")
    # ax.set_xticks(x_ticks)
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.minorticks_off()

    fig, ax = plt.subplots(1, 1)
    ax.plot(x_ticks, speedups, label="Router Update", linestyle=":", marker=".")

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)

    ax.set_xlim([0, 1200])
    ax.set_ylim([0, 1200])

    # ax.set_title("Speed-up of Aggregation and Extension")
    ax.grid(True)
    ax.set_ylabel("Speed-up Factor")
    ax.set_xlabel("# Processes")

    ax.get_xaxis().set_major_formatter('{x:.0f}')
    ax.get_yaxis().set_major_formatter('{x:.0f}')

    ax.legend()


def plot_for_routing():
    data = [extract_durations(BASE_PATH_ROUTING, 2 ** i, "next_time_step") for i in
            range(0, 11)]

    plot_speedup(data)
    plt.show()


if __name__ == "__main__":
    plot_for_routing()
