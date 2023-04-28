import json
from typing import Any

import matplotlib.pyplot as plt


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
