#!/bin/bash --login

#SBATCH -p standard96
#SBATCH -n $nodes
#SBATCH --ntasks-per-node $tasks_per_node
#SBATCH -t 04:00:00
#SBATCH --mail-type=FAIL,STAGE_OUT,INVALID_DEPEND
#SBATCH --job-name=$job_prefix$nodes
#SBATCH --output $job_prefix$nodes.log

module load gcc/9.3.0 llvm/9.0.0 openmpi/gcc.9/4.1.4 metis/5.1.0

echo Process id: $$SLURM_PROCID
echo Cluster Name: $$SLURM_CLUSTER_NAME
echo Job Name: $$SLURM_JOB_NAME
echo Number of Nodes: $$SLURM_JOB_NUM_NODES
echo Number of Tasks: $$SLURM_NTASKS
echo Node Names: $$SLURM_JOB_NODELIST

command="/home/bemheinr/performance_test/rust_q_sim/target/release/mpi_qsim\
 --num-parts $$SLURM_NTASKS\
 --network-file /home/bemheinr/performance_test/berlin-input/berlin-test-network-no-pt.xml.gz\
 --population-file /home/bemheinr/performance_test/berlin-input/$population_file\
 --output-dir /home/bemheinr/performance_test/output/base/$routing_case/output-$$SLURM_NTASKS\
 --sample-size 0.1 $routing_param"

export INERTIAL_FLOW_CUTTER_HOME_DIRECTORY=/home/bemheinr/performance_test/InertialFlowCutter
export RUST_BACKTRACE=full

echo $$command

mpirun $$command