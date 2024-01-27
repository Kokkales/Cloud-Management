from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from workload import WorkloadCreator
from generateReport import ReportGenerator
import os
import sys

# Take the system arguments
# arg1=Number of experiments
# for arg in sys.argv:
#     print(arg)

id=0
file_path = 'simulatorResults.txt'
for i in range(0,1):
    # arg2=Number of erquests
    # arg3=Nimber of batches
    # arg4=Number of sleep time

    # create folder for report
    os.makedirs(f'./plots/experiment{i}/', exist_ok=True)
    workload_creator = WorkloadCreator(request_num=20, batches_num=5, sleep_time=0)  # -1 means random sleep time in each batch
    rpg=ReportGenerator(folder_path=f'./plots/experiment{i}/')


    # Stable Load
    load_type='stable'
    stable_futures = workload_creator.create_load(load_type=load_type)
    wait(stable_futures, return_when=FIRST_COMPLETED)
    rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
    rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
    # for final plot
    stable_tail_latency=workload_creator.get_tail_latency()
    stable_response_times=workload_creator.get_response_times()




    # Normal Load
    load_type='normal'
    normal_futures = workload_creator.create_load(load_type=load_type)
    print(workload_creator.get_tail_latency())
    wait(normal_futures, return_when=FIRST_COMPLETED)
    rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
    rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
    # for final plot
    normal_tail_latency=workload_creator.get_tail_latency()
    normal_response_times=workload_creator.get_response_times()



    # Peak Load
    load_type='peak'
    peak_futures = workload_creator.create_load(load_type=load_type)
    wait(peak_futures, return_when=FIRST_COMPLETED)
    rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
    rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
    # for final plot
    peak_tail_latency=workload_creator.get_tail_latency()
    peak_response_times=workload_creator.get_response_times()

    rpg.plot_table(stable_response_times,stable_tail_latency,normal_response_times,normal_tail_latency,peak_response_times,peak_tail_latency,workload_creator.sleep_time)