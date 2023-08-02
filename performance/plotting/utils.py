import json
from functools import reduce
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# BASE_PATH_ROUTING = "../input/runs_hlrn/base/routing"
# BASE_PATH_NON_ROUTING = "../input/runs_hlrn/base/no-routing"

# BASE_PATH_ROUTING = "../input/runs_hlrn_prep/non-blocking"
# BASE_PATH_NON_ROUTING = "../input/runs_hlrn_prep/non-blocking"

BASE_PATH_ROUTING = "../input/runs_hlrn/base/routing"
BASE_PATH_NON_ROUTING = "../input/runs_hlrn/base/non-blocking"

BASE_PATH_INTERVAL = "../input/runs_hlrn/interval"

GENERAL_EVENTS = ["qsim_step", "mpi_send", "mpi_receive", "mpi_wait_all"]
ROUTING_EVENTS = ["travel_time_aggregating", "travel_time_augmenting", "travel_time_communicating",
                  "travel_time_handling"]

DISPLAY_KEYS = {
    'qsim_step': 'QSim step',
    'mpi_send': 'MPI Send',
    'mpi_receive': 'MPI Receive',
    'travel_time_aggregating': 'Aggregation',
    'travel_time_augmenting': 'Insertion',
    'travel_time_communicating': 'Communication',
    'travel_time_handling': 'Handling',
    'router_customization': 'Router Customization',
    'travel_time_handling_fold': 'Merge Messages',
    'travel_time_handling_clone': 'Clone Network',

}

INTERVALS = [10, 100, 1000, 10000]


def get_display_value_for_key(key):
    value = DISPLAY_KEYS.get(key)
    if value is None:
        return key
    return value


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
    return base_path + "/output-" + str(mpi_slots) + "/trace/mpi_qsim_" + str(slot)


def get_trace_file_path_interval(base_path, interval, slot):
    return base_path + "/" + str(interval) + "/trace/mpi_qsim_" + str(slot)


def get_duration(events, key, first=0) -> np.ndarray:
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return np.array(list(map(lambda e: duration_in_milliseconds(e["duration"]), filtered_events[first::1])))


def get_length(events, key) -> np.ndarray:
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return np.array(list(map(lambda e: int(e["metadata"]["length"]), filtered_events)))


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


def extract_sim_durations_interval(base_path: str, interval: int):
    durations = []
    mpi_slots = 64
    for i in range(0, mpi_slots):
        print("--- INTERVAL " + str(interval) + " | SLOT " + str(i) + " ---")
        events = load_json_event(get_trace_file_path_interval(base_path, interval, i))
        data = get_duration(events, "simulation")
        assert data.size == 1
        durations.append(data[0])
    return np.array(durations)


def extract_qsim_comm_durations(base_path: str, mpi_slots: int, omit_first_event=True) -> Dict[int, pd.DataFrame]:
    result = {}
    first = 1 if omit_first_event else 0
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        duration_qsim_step = get_duration(events, "qsim_step")[first::1]
        duration_mpi_send = get_duration(events, "mpi_send")[first::1]
        duration_mpi_recv = get_duration(events, "mpi_receive")[first::1]
        duration_next_time_step = get_duration(events, "next_time_step")[first::1]
        duration_mpi_wait_all = get_duration(events, "next_time_step")[first::1]
        result[i] = pd.DataFrame(
            {"qsim_step": duration_qsim_step, "mpi_send": duration_mpi_send,
             "mpi_receive": duration_mpi_recv, "next_time_step": duration_next_time_step,
             "mpi_wait_all": duration_mpi_wait_all})
        # print("\n------ SLOT # " + str(i) + " ------")
        # print("\n## QSim Step ##")
        # print(pd.DataFrame(duration_qsim_step).describe())
        # print("\n## MPI Send ##")
        # print(pd.DataFrame(duration_mpi_send).describe())
        # print("\n## MPI Receive ##")
        # print(pd.DataFrame(duration_mpi_recv).describe())
        # print("\n## Next Time Step ##")
        # print(pd.DataFrame(duration_next_time_step).describe())
    return result


def extract_durations(base_path: str, mpi_slots: int, key: str, omit_first_event=True) -> [np.ndarray]:
    result = []
    first = 1 if omit_first_event else 0
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        durations = get_duration(events, key, first)
        result.append(durations)
        print("\n------ SLOT # " + str(i) + " | " + key + " | ------")
        print(pd.DataFrame(durations).describe())
    return result


def extract_durations_interval(base_path: str, interval: int, key: str, omit_first_event=True) -> [np.ndarray]:
    MPI_SLOTS = 64
    result = []
    first = 1 if omit_first_event else 0
    for i in range(0, MPI_SLOTS):
        events = load_json_event(get_trace_file_path_interval(base_path, interval, i))
        durations = get_duration(events, key, first)
        result.append(durations)
        print("\n------ SLOT # " + str(i) + " | " + key + " | ------")
        print(pd.DataFrame(durations).describe(percentiles=[0.9, 0.99]))
    return result


def extract_length(base_path: str, mpi_slots: int, key: str) -> [np.ndarray]:
    result = []
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        mem_sizes = get_length(events, key)
        result.append(mem_sizes)
        print("\n------ SLOT # " + str(i) + " | " + key + " | ------")
        print(pd.DataFrame(mem_sizes).describe())
    return result


def extract_simulation_metadata(base_path: str, mpi_slots: int) -> [dict]:
    result = []
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        simulation_event = list(filter(lambda e: e["key"] == "simulation", events))
        assert len(simulation_event) == 1
        meta = simulation_event[0]["metadata"]
        links = {
            "localLinks": meta["localLinks"]
        }
        result.append(links)
    return result


def extract_duration_by_link(base_path: str, mpi_slots: int, key: str, omit_first_event):
    result = []
    for i in range(0, mpi_slots):
        events = load_json_event(get_trace_file_path(base_path, mpi_slots, i))
        durations = get_duration(events, key, 0)
        result.append(durations)
        print("\n------ SLOT # " + str(i) + " | " + key + " | ------")
        print(pd.DataFrame(durations).describe())
    return result


def get_mean_duration_of_run(run: [np.ndarray]) -> float:
    return reduce(lambda a, b: np.concatenate((a, b), axis=None), run, np.array([])).mean()


def get_mean_list(runs: [[np.ndarray]]) -> [float]:
    return list(map(lambda run: get_mean_duration_of_run(run), runs))


def get_slot_wise_mean_list(data: [np.array]) -> [[float]]:
    return list(map(lambda slot: slot.mean(), data))


def get_slot_wise_number_of_links(data: [[dict]]) -> [[float]]:
    return list(map(lambda run: list(map(lambda slot: slot["localLinks"], run)), data))


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
