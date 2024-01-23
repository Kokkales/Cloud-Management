from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from workload import WorkloadCreator

# Example usage:
workload_creator = WorkloadCreator(load=5)

# Stable Load
stable_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='stable')
wait(stable_futures, return_when=FIRST_COMPLETED)

# Normal Load
normal_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='normal')
wait(normal_futures, return_when=FIRST_COMPLETED)

# Peak Load
peak_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='peak')
wait(peak_futures, return_when=FIRST_COMPLETED)

# Spike Load
spike_futures = workload_creator.create_load(request_num=10, batches_num=5,load_type='spike')
wait(spike_futures, return_when=FIRST_COMPLETED)