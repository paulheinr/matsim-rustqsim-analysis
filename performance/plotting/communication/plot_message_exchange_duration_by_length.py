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

    data = pd.DataFrame(
        data={"duration": np.concatenate(durations, axis=0), "length": np.concatenate(lengths, axis=0),
              "slot": np.repeat(np.arange(0, 2 ** RUN_POWER), len(durations[0]))})

    sns.scatterplot(data=data, x="length", y="duration", hue="slot")
    plt.xlabel("Length")
    plt.ylabel("Duration in ms")
    plt.grid(True, alpha=0.3)

    plt.show()
