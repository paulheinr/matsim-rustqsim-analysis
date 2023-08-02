import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import plotting.utils as utils

if __name__ == '__main__':
    RUN_POWER = 6
    durations = utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** RUN_POWER,
                                        "travel_time_communicating_times",
                                        False)
    lengths = utils.extract_length("../" + utils.BASE_PATH_ROUTING, 2 ** RUN_POWER,
                                   "travel_time_communicating_times")

    all_durations = np.concatenate(durations, axis=0)
    print(pd.DataFrame(all_durations).describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.97, 0.98, 0.99, 0.999]))

    data = pd.DataFrame(
        data={"duration": all_durations, "length": np.concatenate(lengths, axis=0),
              "slot": np.repeat(np.arange(0, 2 ** RUN_POWER), len(durations[0]))})

    # plt.boxplot(all_durations)
    duration_matrix = np.stack(durations)
    length_matrix = np.stack(lengths)

    print("Iteration #1")
    print(pd.DataFrame(duration_matrix[:, 0]).describe())

    fig, ax = plt.subplots(2, 2, sharex='col', gridspec_kw={'width_ratios': [100, 5]})

    ax[1, 1].remove()

    cmap = sns.color_palette("crest", 100)
    sns.heatmap(duration_matrix, cmap=cmap, ax=ax[0, 0], cbar_ax=ax[0, 1])

    length_col = length_matrix[0, :]
    ax[1, 0].plot(list(range(0, 96)), length_col)

    kwargs = {"fontsize": 10}

    ax[0, 0].set_ylabel("Process")
    ax[1, 0].set_ylabel("Length in byte")
    ax[1, 0].set_xlabel("Iteration")
    ax[1, 0].grid(alpha=0.3)

    # ax[1].yaxis.tick_right()
    # ax[1].yaxis.set_label_position("right")

    ax[0, 1].set_title("Duration in ms", **kwargs)
    # ax[1, 0].set_title("Message Length", **kwargs)

    plt.show()
