#!/bin/bash --login
#$$ -cwd
#$$ -N $job_name$nodes
#$$ -o $job_name$nodes.out
#$$ -j y
#$$ -m e
#$$ -M p.heinrich@campus.tu-berlin.de
#$$ -l h_rt=21600
#$$ -l cluster22
#$$ -l mem_free=1G
#$$ -pe ompi22_* $nodes-$nodes

run_command="$base_directory/rust_q_sim/target/release/mpi_qsim\
 --num-parts $nodes\
 --network-file $base_directory$input_directory/berlin-test-network-no-pt.xml.gz\
 --population-file $base_directory$input_directory$population_file\
 --output-dir $base_directory$output_directory$nodes\
 --sample-size 0.1 $routing_param"

export INERTIAL_FLOW_CUTTER_HOME_DIRECTORY=/work/heinrich/InertialFlowCutter
export RUST_BACKTRACE=full
echo $$INERTIAL_FLOW_CUTTER_HOME_DIRECTORY

echo $$run_command

mpirun -np $nodes $$run_command