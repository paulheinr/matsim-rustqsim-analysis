import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import plotting.utils as utils

if __name__ == '__main__':
    RUN_POWER = 7
    durations = utils.extract_durations("../" + utils.BASE_PATH_ROUTING, 2 ** RUN_POWER,
                                        "travel_time_communicating_deserialize",
                                        False)
    lengths = utils.extract_length("../" + utils.BASE_PATH_ROUTING, 2 ** RUN_POWER,
                                   "travel_time_communicating_deserialize")

    data = pd.DataFrame(
        data={"duration": np.concatenate(durations, axis=0), "length": np.concatenate(lengths, axis=0),
              "slot": np.repeat(np.arange(0, 2 ** RUN_POWER), len(durations[0]))})

    # sns.scatterplot(data=data, x="length", y="duration")

    plt.scatter(np.concatenate(lengths, axis=0), np.concatenate(durations, axis=0), c="#1f77b4", marker=".")
    plt.xlabel("Length in bytes")
    plt.ylabel("Duration in ms")
    plt.grid(True, alpha=0.3)

    plt.show()
