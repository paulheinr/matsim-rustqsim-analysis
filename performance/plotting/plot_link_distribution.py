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
    POWER = 10
    # links
    r = range(0, POWER + 1)
    links = [utils.extract_simulation_metadata(utils.BASE_PATH_ROUTING, 2 ** i) for i in r]
    data_points: [np.ndarray] = list(map(lambda l: get_link_array(l), links))

    concatenate = np.concatenate(data_points, axis=1)
    fig, ax = plt.subplots(1, 1)

    ax.scatter(concatenate[1, :], concatenate[0, :], marker=".", color="blue")

    xs_log = np.logspace(0, POWER, base=2, num=POWER + 1)
    xs_lin = np.linspace(0, POWER, num=POWER + 1)

    max_links = list(map(lambda d: np.max(d), data_points))
    min_links = list(map(lambda d: np.min(d[0, :]), data_points))
    ax.scatter(xs_log[1::], max_links[1::], marker=".", color="red", label="Maximum")
    ax.scatter(xs_log[1::], min_links[1::], marker=".", color="green", label="Maximum")

    for i, m in enumerate(max_links):
        ax.annotate(m, (xs_log[i], m), xytext=(1.5, 3), textcoords="offset pixels")
    for i, m in enumerate(min_links):
        if i == 0:
            continue
        ax.annotate(m, (xs_log[i], m), xytext=(1.5, -15), textcoords="offset pixels")

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.get_xaxis().set_major_formatter('{x:.0f}')
    # ax.get_yaxis().set_major_formatter('{x:.0f}')

    ax.set_xlabel("# Processes")
    ax.set_ylabel("# Links")
    ax.grid(True, alpha=0.3)

    ax.legend()

    plt.show()
