import math
import os
from string import Template

TASKS_PER_NODE = 16


def create_run_scripts_for_base(partitions, file_prefix, job_prefix, population_file, routing_param):
    template = open("assets/templates/hlrn/base_template.sh", "r").read()

    routing_case = "no-routing" if routing_param == "" else "routing"

    nodes = math.ceil(partitions / TASKS_PER_NODE)
    tasks_per_node = math.ceil(partitions / nodes)

    text = Template(template).substitute(nodes=nodes, tasks_per_node=tasks_per_node, job_prefix=job_prefix,
                                         routing_param=routing_param, population_file=population_file,
                                         routing_case=routing_case, partitions=partitions)

    write_file(file_prefix + "/" + job_prefix, partitions, text)


def create_run_scripts_for_interval(partitions, file_prefix, interval):
    template = open("assets/templates/hlrn/interval_template.sh", "r").read()

    nodes = math.ceil(partitions / TASKS_PER_NODE)
    tasks_per_node = math.ceil(partitions / nodes)

    text = Template(template).substitute(partitions=partitions, tasks_per_node=tasks_per_node, interval_=interval)

    write_file(file_prefix + "/interval" + str(interval) + "/interval" + str(interval) + "_", partitions, text)


def write_file(file_prefix, number_of_nodes, text):
    filename = file_prefix + str(number_of_nodes) + ".sh"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="\n") as f:
        f.write(text)


if __name__ == '__main__':
    routing_param = "--routing-mode ad-hoc"

    for n in list(map(lambda i: 2 ** i, range(0, 8))):
        create_run_scripts_for_interval(n, "out/scripts/interval", 1)
        create_run_scripts_for_interval(n, "out/scripts/interval", 10)
        create_run_scripts_for_interval(n, "out/scripts/interval", 100)
        create_run_scripts_for_interval(n, "out/scripts/interval", 1000)
        create_run_scripts_for_interval(n, "out/scripts/interval", 10000)
        #
        # create_run_scripts_for_base(n, "out/scripts/base", "base-routing",
        #                             "berlin-10pct-all-plans-no-pt-no-freight-clean.xml.gz", routing_param)
        #
        # create_run_scripts_for_base(n, "out/scripts/base", "base-no-routing",
        #                             "berlin-10pct-all-plans-no-pt-no-freight.xml.gz", "")

        # create_run_scripts_for_blocking_logging(n, "out/scripts/block-logging", "block-base-routing",
        #                                         "berlin-10pct-all-plans-no-pt-no-freight-clean.xml.gz", routing_param)
        #
        # create_run_scripts_for_blocking_logging(n, "out/scripts/block-logging", "block-base-no-routing",
        #                                         "berlin-10pct-all-plans-no-pt-no-freight.xml.gz", "")
