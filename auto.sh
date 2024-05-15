mkdir auto_results

cd draw_multi_cross_tps
python draw_multi_cross_tps.py -w smallbank -c uniform
python draw_multi_cross_tps.py -w smallbank -c skewed
python draw_multi_cross_tps.py -w ycsb -c uniform
python draw_multi_cross_tps.py -w ycsb -c skewed
cp multi-cross-tps-smallbank-uniform.pdf ../auto_results/multi-cross-tps-smallbank-uniform.pdf
cp multi-cross-tps-smallbank-skewed.pdf ../auto_results/multi-cross-tps-smallbank-skewed.pdf
cp multi-cross-tps-ycsb-uniform.pdf ../auto_results/multi-cross-tps-ycsb-uniform.pdf
cp multi-cross-tps-ycsb-skewed.pdf ../auto_results/multi-cross-tps-ycsb-skewed.pdf

cd ..
cd draw_multi_distribute
python draw_multi_distribute.py -w smallbank
python draw_multi_distribute.py -w ycsb
cp smallbank.pdf ../auto_results/multi_distribute_smallbank.pdf
cp ycsb.pdf ../auto_results/multi_distribute_ycsb.pdf

cd ..
cd draw_multi_network
python draw_multi_network_size.py -w smallbank
python draw_multi_network_times.py -w smallbank
cp multi-network-smallbank-size.pdf ../auto_results/multi-network-smallbank-size.pdf
cp multi-network-smallbank.pdf ../auto_results/multi-network-smallbank.pdf

cd ..
cd draw_multi_threads_tps
python draw_multi_threads_tps.py -w smallbank -c uniform
python draw_multi_threads_tps.py -w smallbank -c skewed
python draw_multi_threads_tps.py -w ycsb -c uniform
python draw_multi_threads_tps.py -w ycsb -c skewed
cp multi-threads-tps-smallbank-uniform.pdf ../auto_results/multi-threads-tps-smallbank-uniform.pdf
cp multi-threads-tps-smallbank-skewed.pdf ../auto_results/multi-threads-tps-smallbank-skewed.pdf
cp multi-threads-tps-ycsb-uniform.pdf ../auto_results/multi-threads-tps-ycsb-uniform.pdf
cp multi-threads-tps-ycsb-skewed.pdf ../auto_results/multi-threads-tps-ycsb-skewed.pdf
