import itertools

import numpy as np
from matplotlib import pyplot as plt

import plotting.utils as utils


def get_slot_wise_means(key, power):
    durations = utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** power, key, True)
    slot_wise_means = utils.get_slot_wise_mean_list(durations)
    return np.array(slot_wise_means)


if __name__ == '__main__':
    POWER = 10
    # aggregate data
    mean_aggregation = get_slot_wise_means("travel_time_aggregating", POWER)

    # extension data
    flattened_mean_extension = get_slot_wise_means("travel_time_augmenting", POWER)

    # sync data
    flattened_mean_sync = get_slot_wise_means("travel_time_communicating_lengths", POWER)

    # links
    links = [utils.extract_simulation_metadata("../" + utils.BASE_PATH_ROUTING, 2 ** i) for i in
             range(POWER, POWER + 1)]
    flattened_links = list(map(lambda d: d["localLinks"], itertools.chain.from_iterable(links)))

    plt.scatter(flattened_links, flattened_mean_sync, marker=".", color="blue", label="Synchronization")
    plt.scatter(flattened_links, mean_aggregation, marker=".", color="green", label="Aggregation")
    plt.scatter(flattened_links, flattened_mean_extension, marker=".", color="orange", label="Insertion")
    plt.scatter(flattened_links, flattened_mean_sync + flattened_mean_extension + mean_aggregation, marker="+",
                color="red", label="Sum")

    xseq = np.linspace(min(flattened_links), max(flattened_links), num=10)

    b_sync, a_sync = np.polyfit(flattened_links, flattened_mean_sync, deg=1)
    b_extension, a_extension = np.polyfit(flattened_links, flattened_mean_extension, deg=1)
    print("a = " + str(a_sync) + " | b = " + str(b_sync))
    print("Average duration: " + str(np.mean(flattened_mean_sync)))
    plt.plot(xseq, a_sync + b_sync * xseq, linestyle="dashed", color="blue")
    plt.plot(xseq, a_extension + b_extension * xseq, linestyle="dashed", color="orange")

    plt.xlabel("# Links")
    plt.ylabel("Duration in ms")
    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.show()
