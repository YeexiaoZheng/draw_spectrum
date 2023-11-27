bash run-experiment.sh 1000000 0 11 false true 0
bash run-experiment.sh 1000000 0 11 false true 10

bash run-experiment.sh 1000000 0.9 11 false true 0
bash run-experiment.sh 1000000 0.9 11 false true 10

bash run-experiment.sh 1000000 0.9 11 true true 0
bash run-experiment.sh 1000000 0.9 11 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf0.9-ratio0.pdf -v 28606
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf0.9-ratio10.pdf -v 28606
cd ~/chenzhihao/experiment-threads-tps

bash run-experiment.sh 1000000 1.0 11 false true 0
bash run-experiment.sh 1000000 1.0 11 false true 10

bash run-experiment.sh 1000000 1.0 11 true true 0
bash run-experiment.sh 1000000 1.0 11 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf1.0-ratio0.pdf -v 28606
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf1.0-ratio10.pdf -v 28606
cd ~/chenzhihao/experiment-threads-tps

bash run-experiment.sh 1000000 1.1 11 false true 0
bash run-experiment.sh 1000000 1.1 11 false true 10

bash run-experiment.sh 1000000 1.1 11 true true 0
bash run-experiment.sh 1000000 1.1 11 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf1.1-ratio0.pdf -v 28606
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-11-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/ycsb/zipf1.1-ratio10.pdf -v 28606
cd ~/chenzhihao/experiment-threads-tps

bash run-experiment.sh 1000000 0 15 false true 0
bash run-experiment.sh 1000000 0 15 false true 10

bash run-experiment.sh 1000000 0.9 15 false true 0
bash run-experiment.sh 1000000 0.9 15 false true 10

bash run-experiment.sh 1000000 0.9 15 true true 0
bash run-experiment.sh 1000000 0.9 15 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf0.9-ratio0.pdf -v 73408
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0.9-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf0.9-ratio10.pdf -v 73408
cd ~/chenzhihao/experiment-threads-tps

bash run-experiment.sh 1000000 1.0 15 false true 0
bash run-experiment.sh 1000000 1.0 15 false true 10

bash run-experiment.sh 1000000 1.0 15 true true 0
bash run-experiment.sh 1000000 1.0 15 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf1.0-ratio0.pdf -v 73408
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.0-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf1.0-ratio10.pdf -v 73408
cd ~/chenzhihao/experiment-threads-tps

bash run-experiment.sh 1000000 1.1 15 false true 0
bash run-experiment.sh 1000000 1.1 15 false true 10

bash run-experiment.sh 1000000 1.1 15 true true 0
bash run-experiment.sh 1000000 1.1 15 true true 10

cd ../draw_spectrum/draw_threads_tps
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-0 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-0 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf1.1-ratio0.pdf -v 73408
python ./draw_threads_tps_subplots.py -f1 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-0-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f2 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-15-synthetic-false-two_partitions-true-cold_record_ratio-10 -f3 ~/chenzhihao/experiment-threads-tps/experiment-log-keys-1000000-zipf-1.1-contract-15-synthetic-true-two_partitions-true-cold_record_ratio-10 -o ~/chenzhihao/experiment-threads-tps/draw_output/smallbank/zipf1.1-ratio10.pdf -v 73408
cd ~/chenzhihao/experiment-threads-tps
