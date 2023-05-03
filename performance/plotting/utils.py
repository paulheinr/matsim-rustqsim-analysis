import json
from functools import reduce
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_PATH_ROUTING = "../input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/routing/"
BASE_PATH_NON_ROUTING = "../input/runs_b9f8752f20c85767224605fa9296f3c10d93eb92/no-routing/"

GENERAL_EVENTS = ["qsim_step", "mpi_send", "mpi_receive"]
ROUTING_EVENTS = ["travel_time_collecting", "travel_time_aggregating", "travel_time_send", "travel_time_handling",
                  "router_customization"]


def load_json_event(file):
    data = []
    with open(file) as f:
        for line in f:
            json_line = json.loads(line)
            json_event = json.loads(json_line["fields"]["event"])
            data.append(json_event)
    return data


def filter_events(events: list[Any], key: str) -> list[Any]:
    return list(filter(lambda e: e["key"] == key, events))


def duration_in_milliseconds(duration: Any) -> float:
    seconds = duration["secs"]
    nanoseconds = duration["nanos"]
    return seconds * 1000 + nanoseconds / 1000000


def get_trace_file_path(base_path, mpi_slots, slot) -> str:
    return base_path + "/trace" + str(mpi_slots) + "/mpi_qsim_" + str(slot)


def get_duration(events, key) -> np.ndarray:
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return np.array(list(map(lambda e: duration_in_milliseconds(e["duration"]), filtered_events)))


def extract_sim_durations(base_path: str, max_power: int) -> Dict[int, np.ndarray]:
    sim_durations_by_mpi_slots = {}
    for mpi_slots in (2 ** p for p in range(0, max_power)):
        sim_durations_fixed_slot_amount = []

        for i in range(0, mpi_slots):
            events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
            data = get_duration(events, "simulation")
            assert data.size == 1
            sim_durations_fixed_slot_amount.append(data[0])

        sim_durations_by_mpi_slots[mpi_slots] = np.array(sim_durations_fixed_slot_amount)

    return sim_durations_by_mpi_slots


def extract_qsim_comm_durations(base_path: str, mpi_slots: int, omit_first_event=True) -> Dict[int, pd.DataFrame]:
    result = {}
    first = 1 if omit_first_event else 0
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        duration_qsim_step = get_duration(events, "qsim_step")[first::1]
        duration_mpi_send = get_duration(events, "mpi_send")[first::1]
        duration_mpi_recv = get_duration(events, "mpi_receive")[first::1]
        result[i] = pd.DataFrame(
            {"qsim_step": duration_qsim_step, "mpi_send": duration_mpi_send,
             "mpi_receive": duration_mpi_recv})
        print("\n------ SLOT # " + str(i) + " ------")
        print("\n## QSim Step ##")
        print(pd.DataFrame(duration_qsim_step).describe())
        print("\n## MPI Send ##")
        print(pd.DataFrame(duration_mpi_send).describe())
        print("\n## MPI Receive ##")
        print(pd.DataFrame(duration_mpi_recv).describe())
    return result


def extract_durations(base_path: str, mpi_slots: int, key: str, omit_first_event=True) -> [np.ndarray]:
    result = []
    first = 1 if omit_first_event else 0
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        durations = get_duration(events[first::1], key)
        result.append(durations)
        print("\n------ SLOT # " + str(i) + " | " + key + " | ------")
        print(pd.DataFrame(durations).describe())
    return result


def get_mean_duration_of_run(data: [np.ndarray]) -> float:
    return reduce(lambda a, b: np.concatenate((a, b), axis=None), data, np.array([])).mean()


def get_mean_list(data: [[np.ndarray]]) -> [float]:
    return list(map(lambda d: get_mean_duration_of_run(d), data))


def get_speedup_list(data: [[np.ndarray]]) -> [float]:
    mean_list = get_mean_list(data)
    return [mean_list[0] / m for m in mean_list]


def plot_millis_by_updates(file: str, key: str):
    events = load_json_event(file)
    send_events = filter_events(events, key)
    x = []
    y = []
    for e in send_events:
        x.append(e["metadata"]["updates"])
        y.append(duration_in_milliseconds(e["duration"]))

    plt.plot(x, y, ".", color="black")
    plt.title("File: " + file + " | Key: " + key)
    plt.show()


def plot_millis_histogram(file: str, key: str):
    events = load_json_event(file)
    send_events = filter_events(events, key)
    y = []
    for e in send_events:
        y.append(duration_in_milliseconds(e["duration"]))

    plt.hist(y)
    plt.title("File: " + file + " | Key: " + key)
    plt.show()


if __name__ == '__main__':
    plot_millis_histogram("input/mpi_qsim_0", "travel_time_aggregation")
    plot_millis_histogram("input/mpi_qsim_1", "travel_time_aggregation")

    plot_millis_by_updates("input/mpi_qsim_0", "travel_time_handling")
    plot_millis_by_updates("input/mpi_qsim_1", "travel_time_handling")
