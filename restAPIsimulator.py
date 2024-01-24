from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from workload import WorkloadCreator

def printResultsPerBatch():
    print('-------BATCH-------')
    print(f'CPU: {workload_creator.get_cpu_each_batch()}')
    print(f'RAM: {workload_creator.get_ram_each_batch()}')
    print(f'BW: {workload_creator.get_bw_each_batch()}')
    print('-------REQUESTS-------')
    print(f'CPU: {workload_creator.get_cpu_each_request()}')
    print(f'RAM: {workload_creator.get_ram_each_request()}')
    print(f'BW: {workload_creator.get_bw_each_request()}')
    print('-------POST REQUEST-------')
    print(f'Avg CPU: {workload_creator.get_cpu_average_method_post()}')
    print(f'Avg RAM: {workload_creator.get_ram_average_method_post()}')
    print(f'Avg BW: {workload_creator.get_bw_average_method_post()}')
    print('-------GET REQUEST-------')
    print(f'Avg CPU: {workload_creator.get_cpu_average_method_get()}')
    print(f'Avg RAM: {workload_creator.get_ram_average_method_get()}')
    print(f'Avg BW: {workload_creator.get_bw_average_method_get()}')
    print('-------PUT REQUEST-------')
    print(f'Avg CPU: {workload_creator.get_cpu_average_method_put()}')
    print(f'Avg RAM: {workload_creator.get_ram_average_method_put()}')
    print(f'Avg BW: {workload_creator.get_bw_average_method_put()}')
    print('-------DELETE REQUEST-------')
    print(f'Avg CPU: {workload_creator.get_cpu_average_method_delete()}')
    print(f'Avg RAM: {workload_creator.get_ram_average_method_delete()}')
    print(f'Avg BW: {workload_creator.get_bw_average_method_delete()}')
    print('\n')
# Example usage:
workload_creator = WorkloadCreator()

# Stable Load
stable_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='stable')
wait(stable_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# Normal Load
normal_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='normal')
wait(normal_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# Peak Load
peak_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='peak')
wait(peak_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# Spike Load
spike_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='spike')
wait(spike_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()