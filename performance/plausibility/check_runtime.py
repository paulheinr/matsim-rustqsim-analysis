import pandas as pd
from matplotlib import pyplot as plt

import plotting.utils as utils


def get_errors_of_run(qsim_comm_durations, measured_times):
    errors_of_slot = []
    estimated_times = []
    for slot, qsim_comm_of_slot in qsim_comm_durations.items():
        measured_time = measured_times[slot]
        estimated_time = (qsim_comm_of_slot["qsim_step"].sum()) * tracing_interval + qsim_comm_of_slot[
            "next_time_step"].sum()
        estimated_times.append(estimated_time)

        error = (estimated_time - measured_time) * 100 / measured_time
        errors_of_slot.append(error)

        print("------ Result slot " + str(slot) + " ------")
        print("Measured time (ms): " + str(measured_time))
        print("Estimated time (ms): " + str(estimated_time))
        print("Error of estimation (%): " + str(error))

    plt.hist(errors_of_slot, alpha=0.7)
    plt.title("Estimation errors of run with " + str(len(errors_of_slot)) + " slots.")
    # plt.show()

    return estimated_times


if __name__ == '__main__':
    tracing_interval = 900

    qsim_comm_durations: [dict[int, pd.DataFrame]] = [
        utils.extract_qsim_comm_durations(utils.BASE_PATH_ROUTING, 2 ** i) for i in range(0, 7)]

    measured_times = utils.extract_sim_durations(utils.BASE_PATH_ROUTING, 7)

    for d in qsim_comm_durations:
        number_of_slots = len(d)

        print("------ Run with #MPI-Slots: " + str(number_of_slots) + " ------")
        estimated_times = get_errors_of_run(d, measured_times[number_of_slots])
        print("Overall estimation error (%): " + str(
            (sum(estimated_times) - sum(measured_times[number_of_slots])) * 100 / sum(measured_times[number_of_slots])))
