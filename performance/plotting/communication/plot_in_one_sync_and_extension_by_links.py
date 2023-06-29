import itertools

import numpy as np
from matplotlib import pyplot as plt

import plotting.utils as utils

if __name__ == '__main__':
    range = range(6, 7)
    # extension data
    extension_durations = [
        utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** i, "travel_time_augmenting", True) for i
        in range]
    slot_wise_means_extension = utils.get_slot_wise_mean_list(extension_durations)
    flattened_mean_extension = np.array(list(itertools.chain.from_iterable(slot_wise_means_extension)))

    # sync data
    sync_durations = [
        utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** i, "travel_time_communicating_lengths", True)
        for i in range]
    slot_wise_means_sync = utils.get_slot_wise_mean_list(sync_durations)
    flattened_mean_sync = np.array(list(itertools.chain.from_iterable(slot_wise_means_sync)))

    # links
    links = [utils.extract_simulation_metadata("../" + utils.BASE_PATH_ROUTING, 2 ** i) for i in range]
    flattened_links = list(map(lambda d: d["localLinks"], itertools.chain.from_iterable(links)))

    plt.scatter(flattened_links, flattened_mean_sync, marker=".", color="blue", label="Synchronization")
    plt.scatter(flattened_links, flattened_mean_extension, marker=".", color="orange", label="Extension")
    plt.scatter(flattened_links, flattened_mean_sync + flattened_mean_extension, marker="+", color="red", label="Sum")

    xseq = np.linspace(min(flattened_links), max(flattened_links), num=10)

    b_sync, a_sync = np.polyfit(flattened_links, flattened_mean_sync, deg=1)
    b_extension, a_extension = np.polyfit(flattened_links, flattened_mean_extension, deg=1)
    print("a = " + str(a_sync) + " | b = " + str(b_sync))
    print("Average duration: " + str(np.mean(flattened_mean_sync)))
    plt.plot(xseq, a_sync + b_sync * xseq, linestyle="dashed", color="blue")
    plt.plot(xseq, a_extension + b_extension * xseq, linestyle="dashed", color="orange")

    plt.xlabel("Number of Links")
    plt.ylabel("Duration in ms")
    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.show()
