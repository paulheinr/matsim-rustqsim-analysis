import utils


def plot():
    return 0


def get_duration(events, key):
    filtered_events = list(filter(lambda e: e["key"] == key, events))
    return list(map(lambda e: utils.duration_in_milliseconds(e["duration"]), filtered_events))


if __name__ == '__main__':
    data = []
    for i in range(0, 8):
        events = utils.load_json_event("./assets/trace8/" + str(i))
        data = [get_duration(events, "qsim_step"), get_duration(events, "mpi_send"),
                get_duration(events, "mpi_receive")]

    plot()
