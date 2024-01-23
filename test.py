from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from BasicMonitoring import Monitoring
import requests
import time
import random
import psutil
import threading

class WorkloadCreator():
    def __init__(self, load):
        self.load = load

    def create_batch(self, batch_size):
        batch = [
            {'method': 'GET', 'endpoint': 'get'},
            {'method': 'POST', 'endpoint': 'post', 'payload': {'key': 'value'}},
            {'method': 'DELETE', 'endpoint': 'delete'},
            {'method': 'PUT', 'endpoint': 'put', 'payload': {'key': 'value'}},
        ]
        return [random.choice(batch) for _ in range(batch_size)]

    def create_load(self, request_num, batches_num, sleep_time=True,load_type='normal'):
        print(f"{load_type}------------------------------------------")
        futures = []
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]
        for i in range(batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0

            if load_type=='stable':
                batch_size = request_num // batches_num
            elif load_type=='normal':
                batch_size = random.randint(1, request_num // batches_num)
            elif load_type=='peak':
                batch_size = request_num // batches_num
                if i == random.randint(1,9):
                    batch_size *= 3  # Triple the requests in the peak batch
            else:
                batch_size = request_num // batches_num

                if i == random.randint(1,9):
                    batch_size *= 3  # Triple the requests in the spike batch

            batch = self.create_batch(batch_size)
            for _ in range(batch_size):
                with ThreadPoolExecutor() as executor:
                    mon_obj = Monitoring([], [], [], threading.Event())
                    request = random.choice(batch)
                    future = executor.submit(run_request_with_monitoring, request, mon_obj)
                    futures.append(future)
                    cpu,ram,bw=future.result()
                    # print("::::",cpu,ram,bw)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)

            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means)
        return futures

    # Creates equal sized batches
    def create_stable_load(self, request_num, batches_num, sleep_time=True):
        print("STABLE LOAD------------------------------------------")
        futures = []
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]
        for i in range(batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0

            # print(f"\nBatch Number: {i}")
            batch_size = request_num // batches_num

            batch = self.create_batch(batch_size)
            for _ in range(batch_size):
                with ThreadPoolExecutor() as executor:
                    mon_obj = Monitoring([], [], [], threading.Event())
                    request = random.choice(batch)
                    future = executor.submit(run_request_with_monitoring, request, mon_obj)
                    futures.append(future)
                    cpu,ram,bw=future.result()
                    # print("::::",cpu,ram,bw)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)

            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means)
        return futures

    # Creates random
    def create_normal_load(self, request_num, batches_num, sleep_time=True):
        print("NORMAL LOAD------------------------------------------")
        futures = []
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]
        for i in range(batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0

            # print(f"\nBatch Number: {i}")
            batch_size = random.randint(1, request_num // batches_num)

            batch = self.create_batch(batch_size)
            for _ in range(batch_size):
                with ThreadPoolExecutor() as executor:
                    mon_obj = Monitoring([], [], [], threading.Event())
                    request = random.choice(batch)
                    future = executor.submit(run_request_with_monitoring, request, mon_obj)
                    futures.append(future)
                    cpu,ram,bw=future.result()
                    # print("::::",cpu,ram,bw)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)
            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means)
        return futures

    def create_peak_load(self, request_num, batches_num, peak_batch_num, sleep_time=True):
        print("PEAK LOAD------------------------------------------")
        futures = []
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]
        for i in range(batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0
            # print(f"\nBatch Number: {i}")
            batch_size = request_num // batches_num

            if i == peak_batch_num:
                batch_size *= 3  # Triple the requests in the peak batch

            batch = self.create_batch(batch_size)
            for _ in range(batch_size):
                with ThreadPoolExecutor() as executor:
                    mon_obj = Monitoring([], [], [], threading.Event())
                    request = random.choice(batch)
                    future = executor.submit(run_request_with_monitoring, request, mon_obj)
                    futures.append(future)
                    cpu,ram,bw=future.result()
                    # print("::::",cpu,ram,bw)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)

            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means)

        return futures

    def create_spike_load(self, request_num, batches_num, spike_batch_num, sleep_time=True):
        print("SPIKE LOAD------------------------------------------")
        futures = []
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]
        for i in range(batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0
            # print(f"\nBatch Number: {i}")
            batch_size = request_num // batches_num

            if i == spike_batch_num:
                batch_size *= 3  # Triple the requests in the spike batch

            batch = self.create_batch(batch_size)
            for _ in range(batch_size):
                with ThreadPoolExecutor() as executor:
                    mon_obj = Monitoring([], [], [], threading.Event())
                    request = random.choice(batch)
                    future = executor.submit(run_request_with_monitoring, request, mon_obj)
                    futures.append(future)
                    cpu,ram,bw=future.result()
                    # print("::::",cpu,ram,bw)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)

            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means)
        return futures

    def printResults(self,cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means):
        print(f'Average CPU per batch:{cpu_per_batch_means}')
        print(f'Average RAM per batch:{ram_per_batch_means}')
        print(f'Average BW per batch:{bw_per_batch_means}')

        print(f'Average CPU of all: {sum(cpu_per_batch_means)/len(cpu_per_batch_means)}')
        print(f'Average RAM of all: {sum(ram_per_batch_means)/len(ram_per_batch_means)}')
        print(f'Average BW of all: {sum(bw_per_batch_means)/len(bw_per_batch_means)}\n')

def create_request(endpoint, method, payload):
    url = f"http://localhost:5000/{endpoint}"
    headers = {'Content-Type': 'application/json'}

    if method == 'GET':
        resp = requests.get(url, headers=headers)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, json=payload)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers)
    elif method == 'PUT':
        resp = requests.put(url, headers=headers, json=payload)
    return resp

response_times = []
lock = threading.Lock()
def run_request_with_monitoring(request, mon_obj):
    method = request['method']
    endpoint = request['endpoint']
    payload = request.get('payload')

    mon_obj.event.clear()
    cpu_monitoring_thread = threading.Thread(target=mon_obj.monitor_cpu)
    cpu_monitoring_thread.start()
    mon_obj.event.clear()
    ram_monitoring_thread = threading.Thread(target=mon_obj.monitor_ram)
    ram_monitoring_thread.start()
    mon_obj.event.clear()
    bw_monitoring_thread = threading.Thread(target=mon_obj.monitor_bw)
    bw_monitoring_thread.start()

    start_time = time.time()
    response = create_request(endpoint, method, payload)
    end_time = time.time()

    mon_obj.event.set()
    cpu_monitoring_thread.join()
    ram_monitoring_thread.join()
    bw_monitoring_thread.join()

    response_time = end_time - start_time

    with lock:
        response_times.append(response_time)

    # print(f"Request {method} {endpoint}:\nStatus Code: {response.status_code}\nResponse Time: {response_time} (sec)\nCPU: {mon_obj.cpu_util} (%)\nRAM: {mon_obj.ram_util} (%)\nBandwidth: {mon_obj.bw_util} (bits/sec)")

    return sum(mon_obj.cpu_util)/len(mon_obj.cpu_util),sum(mon_obj.ram_util)/len(mon_obj.ram_util),sum(mon_obj.bw_util)/len(mon_obj.bw_util)

# Example usage:
workload_creator = WorkloadCreator(load=5)

# # Stable Load
# stable_futures = workload_creator.create_stable_load(request_num=10, batches_num=5)
# wait(stable_futures, return_when=FIRST_COMPLETED)

# # Normal Load
# normal_futures = workload_creator.create_normal_load(request_num=10, batches_num=5)
# wait(normal_futures, return_when=FIRST_COMPLETED)

# # Peak Load
# peak_futures = workload_creator.create_peak_load(request_num=10, batches_num=5, peak_batch_num=2)
# wait(peak_futures, return_when=FIRST_COMPLETED)

# # Spike Load
# spike_futures = workload_creator.create_spike_load(request_num=10, batches_num=5, spike_batch_num=3)
# wait(spike_futures, return_when=FIRST_COMPLETED)

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