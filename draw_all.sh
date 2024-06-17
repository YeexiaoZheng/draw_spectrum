cd draw_checkpoint
python draw_checkpoint.py

cd ..

cd draw_latency
python draw_latency.py -w smallbank -c skewed -t 36
python draw_latency.py -w ycsb -c skewed -t 36
python draw_latency.py -w tpcc -c skewed -t 36
python draw_block_latency.py -w smallbank -c skewed -t 36
python draw_block_latency.py -w ycsb -c skewed -t 36
python draw_block_latency.py -w tpcc -c skewed -t 36

cd ..
cd draw_memory
python draw_memory.py -w ycsb -c skewed -t 36

cd ..
cd draw_skew_abort
python draw_skew_abort.py -w pre -t 36

cd ..
cd draw_skew_op
python draw_skew_op.py -w smallbank -t 36
python draw_skew_op.py -w ycsb -t 36
python draw_skew_op.py -w tpcc -t 36

cd ..
cd draw_skew_tps
python draw_skew_tps.py -w smallbank -t 36
python draw_skew_tps.py -w ycsb -t 36
python draw_skew_tps.py -w tpcc -t 36
python draw_skew_tps.py -w pre -t 36

cd ..
cd draw_threads_tps
python draw_threads_tps.py -w smallbank -c skewed
python draw_threads_tps.py -w ycsb -c skewed
python draw_threads_tps.py -w tpcc -c 20orderlines
python draw_threads_tps.py -w smallbank -c uniform
python draw_threads_tps.py -w ycsb -c uniform
python draw_threads_tps.py -w tpcc -c 10orderlines
python draw_threads_tps.py -w ycsb -c pres
python draw_threads_tps.py -w ycsb -c compare

cd ..
