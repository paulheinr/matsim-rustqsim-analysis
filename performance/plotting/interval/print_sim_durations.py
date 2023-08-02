import numpy as np
import pandas as pd

import plotting.utils as utils


def print_sim_durations():
    means = []
    for i in utils.INTERVALS:
        durations = utils.extract_sim_durations_interval("../" + utils.BASE_PATH_INTERVAL, i)
        print("--- INTERVAL " + str(i) + " ---")
        print(pd.DataFrame(durations).describe(percentiles=[0.9, 0.99]))
        means.append(durations.mean())
    print("--- MEAN INTERVALS ---")
    print(np.around(means, 2))


def print_sim_duration_minus_update():
    sim_durations = np.array([3076184.22, 647032.97, 395140.03, 369638.01])
    update_durations = np.array([310.37, 318.92, 316.19, 330.97])
    number_of_updates = np.floor((60 * 60 * 24) / np.array(utils.INTERVALS))
    minus = (np.multiply(update_durations, number_of_updates))
    result = sim_durations - minus

    print("--- NUMBER OF UPDATES ---")
    print(number_of_updates)
    print("--- RESULT ---")
    print(result)


if __name__ == '__main__':
    print_sim_duration_minus_update()
