from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from workload import WorkloadCreator
from plotter import Plotter

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
    print(f'Avg BW: {workload_creator.get_bw_average_method_delete()}\n')
    print(f'Response Time:: {workload_creator.get_response_times()}')
    print('\n')
    visualiser.plot_batch_oriented(workload_creator.get_cpu_each_batch(),workload_creator.get_ram_each_batch(),workload_creator.get_bw_each_batch())


workload_creator = WorkloadCreator(request_num=10,batches_num=5,sleep_time=0)
visualiser=Plotter(request_num=workload_creator.get_request_number(),batches_num=workload_creator.get_batches_number(),sleep_time=0)

# Stable Load
stable_futures = workload_creator.create_load(load_type='stable')
wait(stable_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# Normal Load
normal_futures = workload_creator.create_load(load_type='normal')
wait(normal_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# Peak Load
peak_futures = workload_creator.create_load(load_type='peak')
wait(peak_futures, return_when=FIRST_COMPLETED)
printResultsPerBatch()

# # Spike Load
# spike_futures = workload_creator.create_load(load_type='spike')
# wait(spike_futures, return_when=FIRST_COMPLETED)
# printResultsPerBatch()