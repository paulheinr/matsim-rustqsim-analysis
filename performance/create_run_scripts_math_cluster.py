import os
from string import Template

BASE_DIRECTORY = "/net/work/heinrich"
INPUT_DIRECTORY = "/runs/berlin-test-input/"
OUTPUT_DIRECTORY = "/runs/berlin-test-output/"


def create_run_scripts(number_of_nodes, file_prefix, job_name, population_file, routing_param):
    template = open("assets/templates/math_cluster/run-berlin-test-template.sh", "r").read()
    text = Template(template).substitute(base_directory=BASE_DIRECTORY, input_directory=INPUT_DIRECTORY,
                                         output_directory=OUTPUT_DIRECTORY + job_name, nodes=number_of_nodes,
                                         job_name=job_name, population_file=population_file,
                                         routing_param=routing_param)

    write_file(file_prefix, number_of_nodes, text)


def write_file(file_prefix, number_of_nodes, text):
    filename = file_prefix + str(number_of_nodes) + ".sh"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="\n") as f:
        f.write(text)


if __name__ == '__main__':
    for n in list(map(lambda i: 2 ** i, range(0, 9))):
        routing_param = "--routing-mode ad-hoc"

        create_run_scripts(n, "out/scripts/run-berlin-routing", "berlin-test-routing",
                           "berlin-10pct-all-plans-no-pt-clean-no-freight.xml.gz", routing_param)

        create_run_scripts(n, "out/scripts/run-berlin-no-routing", "berlin-test-no-routing",
                           "berlin-10pct-all-plans-no-pt.xml.gz", "")
