from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from Classes.workload import WorkloadCreator
from Classes.generateReport import ReportGenerator
import os
import sys

if len(sys.argv)!=4:
    print("python3 restAPIsimulator.py <#of experiments> <a/n/s/p> <stress/nostress>")
    sys.exit()

num_of_exp=int(sys.argv[1])
mode=sys.argv[2]
isStressing=sys.argv[3]

stress_combinations=[]
if isStressing=='stress':
    for i in range(1, 4):
        stress_value = i * 100
        time_value = i * 5
        factor_value = i
        stress_combinations.append((stress_value, time_value, factor_value))
    print(stress_combinations)


id=0
file_path = './Other_files/simulatorResults.txt'
for i in range(0,num_of_exp):
    # ask for input #number of requests, #number of batches, sleep_time
    if isStressing!='stress':
        number_of_req = int(input("Number of requests: "))
        number_of_batches = int(input("Number of batches: "))
        sleep_time_se = int(input("Sleep time: "))
        user_combinations=[(number_of_req,number_of_batches,sleep_time_se)]


    if isStressing=='stress':
        combinations=stress_combinations
    else:
        combinations=user_combinations

    for count,(j,k,l) in enumerate(combinations):
        print(f'Experiment {count}\n')
        req,batches,sleep_t=j,k,l
        # create folder for report
        os.makedirs(f'./Plots/', exist_ok=True)
        os.makedirs(f'./Plots/experiment{i}/', exist_ok=True)
        workload_creator = WorkloadCreator(request_num=req, batches_num=batches, sleep_time=sleep_t)  # -1 means random sleep time in each batch
        rpg=ReportGenerator(folder_path=f'./plots/experiment{i}/')

        if mode=='a' or mode=='s':
            # Stable Load
            load_type='stable'
            stable_futures = workload_creator.create_load(load_type=load_type)
            # wait(stable_futures, return_when=FIRST_COMPLETED)zzzzz
            rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
            rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
            # for final plot
            stable_tail_latency=workload_creator.get_tail_latency()
            stable_response_times=workload_creator.get_response_times()



        if mode=='a' or mode=='n':
            # Normal Load
            load_type='normal'
            normal_futures = workload_creator.create_load(load_type=load_type)
            wait(normal_futures, return_when=FIRST_COMPLETED)
            rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
            rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
            # for final plot
            normal_tail_latency=workload_creator.get_tail_latency()
            normal_response_times=workload_creator.get_response_times()


        if mode=='a' or mode=='p':
            # Peak Load
            load_type='peak'
            peak_futures = workload_creator.create_load(load_type=load_type)
            wait(peak_futures, return_when=FIRST_COMPLETED)
            rpg.save_to_file(id+1,file_path,load_type,workload_creator.get_timestamp(),workload_creator.get_request_number(),workload_creator.get_batches_number(),workload_creator.sleep_time,workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch(),workload_creator.get_cpu_each_request(),workload_creator.get_ram_each_request(),workload_creator.get_bw_each_request(),workload_creator.get_cpu_average_method_post(),workload_creator.get_ram_average_method_post(),workload_creator.get_bw_average_method_post(),workload_creator.get_cpu_average_method_get(),workload_creator.get_ram_average_method_get(),workload_creator.get_bw_average_method_get(),workload_creator.get_cpu_average_method_put(),workload_creator.get_ram_average_method_put(),workload_creator.get_bw_average_method_put(),workload_creator.get_cpu_average_method_delete(),workload_creator.get_ram_average_method_delete(),workload_creator.get_bw_average_method_delete(),workload_creator.get_response_times(),workload_creator.get_tail_latency())
            rpg.plot_diagrams(file_path=file_path,load_type=load_type,sleep_time=workload_creator.sleep_time)
            # for final plot
            peak_tail_latency=workload_creator.get_tail_latency()
            peak_response_times=workload_creator.get_response_times()
        if mode=='a':
            rpg.plot_table(stable_response_times,stable_tail_latency,normal_response_times,normal_tail_latency,peak_response_times,peak_tail_latency,workload_creator.sleep_time)