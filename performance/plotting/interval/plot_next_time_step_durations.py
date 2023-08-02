import numpy as np
from matplotlib import pyplot as plt

import plotting.utils as utils


def get_link_array(link_dict_list):
    number_of_processes = len(link_dict_list)
    link_list = list(map(lambda d: d["localLinks"], link_dict_list))
    process_list = [number_of_processes] * number_of_processes
    array = np.array([link_list, process_list])
    return array


if __name__ == '__main__':
    POWER = 7
    times = []
    for i in utils.INTERVALS:
        all_next_time_step_of_interval = np.concatenate(
            utils.extract_durations_interval("../" + utils.BASE_PATH_INTERVAL, i, "next_time_step", True))
        times.append(all_next_time_step_of_interval)

    fig, ax = plt.subplots(1, 1)

    ax.boxplot(times, labels=utils.INTERVALS, showmeans=True)

    # ax.set_xscale("log", base=2)
    # ax.set_yscale("log", base=2)
    # ax.get_xaxis().set_major_formatter('{x:.0f}')
    # ax.get_yaxis().set_major_formatter('{x:.0f}')

    means = np.array(list(map(lambda t: t.mean(), times)))
    print(np.around(means, 2))

    ax.set_xlabel("Interval")
    ax.set_ylabel("Duration in ms")
    ax.grid(True, alpha=0.3)

    # ax.legend()

    plt.show()
