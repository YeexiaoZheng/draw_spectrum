# f1=experiment-log-keys-1000000-zipf-0.9-contract-11-synthetic-true-two_partitions-true-cold_record_ratio-1
# value="$(cat $f1 | head -n 8 | grep "average commit:")"
# value=${value#*: }
# value=${value%% *}
# echo "$value"

experiment_root="/home/z/chenzhihao/experiment-threads-tps"

# 基本不变
keys=1000000
two_partitions=true

# 调整ratio
cold_record_ratio=0

##### YCSB #####
contract=11
contract_str="ycsb"

zipf=0
synthetic=false
f1=$experiment_root/experiment-log-keys-$keys-zipf-$zipf-contract-$contract-synthetic-$synthetic-two_partitions-$two_partitions-cold_record_ratio-$cold_record_ratio

zipf=0.999
synthetic=false
f2="$experiment_root/experiment-log-keys-$keys-zipf-$zipf-contract-$contract-synthetic-$synthetic-two_partitions-$two_partitions-cold_record_ratio-$cold_record_ratio"

synthetic=true
f3="$experiment_root/experiment-log-keys-$keys-zipf-$zipf-contract-$contract-synthetic-$synthetic-two_partitions-$two_partitions-cold_record_ratio-$cold_record_ratio"

value=$(cat $f1 | head -n 8 | grep "average commit:")
value=${value#*: }
value=${value%% *}
echo $value
output="$experiment_root/draw_output/$contract_str/zipf$zipf-ratio$ratio.pdf"
python ./draw_threads_tps_subplots.py -f1 $f1 -f2 $f2 -f3 $f3 -o $output -v $value