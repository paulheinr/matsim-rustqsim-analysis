import itertools

import numpy as np
from matplotlib import pyplot as plt

import plotting.utils as utils

if __name__ == '__main__':
    durations = [utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** i, "travel_time_augmenting", False) for i
                 in range(6, 7)]
    slot_wise_means = utils.get_slot_wise_mean_list(durations)
    flattened_mean = list(itertools.chain.from_iterable(slot_wise_means))

    links = [utils.extract_simulation_metadata("../" + utils.BASE_PATH_ROUTING, 2 ** i) for i in range(6, 7)]
    flattened_links = list(map(lambda d: d["localLinks"], itertools.chain.from_iterable(links)))

    plt.scatter(flattened_links, flattened_mean, marker=".")

    b, a = np.polyfit(flattened_links, flattened_mean, deg=1)
    print("a = " + str(a) + " | b = " + str(b))
    print("Average duration: " + str(np.mean(flattened_mean)))
    xseq = np.linspace(min(flattened_links), max(flattened_links), num=10)
    plt.plot(xseq, a + b * xseq, linestyle="dashed")

    plt.xlabel("Number of Links")
    plt.ylabel("Duration in ms")
    plt.grid(True, alpha=0.3)

    plt.show()
