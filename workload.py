from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from BasicMonitoring import Monitoring
import requests
import time
import random
import psutil
import threading

class WorkloadCreator():
    def __init__(self,cpu_each_batch=[],ram_each_batch=[],bw_each_batch=[],cpu_each_request=[],ram_each_request=[],bw_each_request=[],cpu_average_method_post=0,ram_average_method_post=0,bw_average_method_post=0,cpu_average_method_get=0,ram_average_method_get=0,bw_average_method_get=0,cpu_average_method_put=0,ram_average_method_put=0,bw_average_method_put=0,cpu_average_method_delete=0,ram_average_method_delete=0,bw_average_method_delete=0):
        # Batch
        self.cpu_each_batch=cpu_each_batch
        self.ram_each_batch=ram_each_batch
        self.bw_each_batch=bw_each_batch
        # Request
        self.cpu_each_request=cpu_each_request
        self.ram_each_request=ram_each_request
        self.bw_each_request=bw_each_request
        # Post
        self.cpu_average_method_post=cpu_average_method_post
        self.ram_average_method_post=ram_average_method_post
        self.bw_average_method_post=bw_average_method_post
        # Get
        self.cpu_average_method_get=cpu_average_method_get
        self.ram_average_method_get=ram_average_method_get
        self.bw_average_method_get=bw_average_method_get
        # PUT
        self.cpu_average_method_put=cpu_average_method_put
        self.ram_average_method_put=ram_average_method_put
        self.bw_average_method_put=bw_average_method_put
        # DELETE
        self.cpu_average_method_delete=cpu_average_method_delete
        self.ram_average_method_delete=ram_average_method_delete
        self.bw_average_method_delete=bw_average_method_delete

    # Getter method for cpu_each_batch
    def get_cpu_each_batch(self):
        return self.cpu_each_batch

    # Getter method for ram_each_batch
    def get_ram_each_batch(self):
        return self.ram_each_batch

    # Getter method for bw_each_batch
    def get_bw_each_batch(self):
        return self.bw_each_batch

    def get_cpu_each_request(self):
        return self.cpu_each_request

    def get_ram_each_request(self):
        return self.ram_each_request

    def get_bw_each_request(self):
        return self.bw_each_request

    # Getter methods for cpu_average_method_post
    def get_cpu_average_method_post(self):
        return self.cpu_average_method_post

    # Getter methods for ram_average_method_post
    def get_ram_average_method_post(self):
        return self.ram_average_method_post

    # Getter methods for bw_average_method_post
    def get_bw_average_method_post(self):
        return self.bw_average_method_post

    # Getter methods for cpu_average_method_get
    def get_cpu_average_method_get(self):
        return self.cpu_average_method_get

    # Getter methods for ram_average_method_get
    def get_ram_average_method_get(self):
        return self.ram_average_method_get

    # Getter methods for bw_average_method_get
    def get_bw_average_method_get(self):
        return self.bw_average_method_get

    # Getter methods for cpu_average_method_put
    def get_cpu_average_method_put(self):
        return self.cpu_average_method_put

    # Getter methods for ram_average_method_put
    def get_ram_average_method_put(self):
        return self.ram_average_method_put

    # Getter methods for bw_average_method_put
    def get_bw_average_method_put(self):
        return self.bw_average_method_put

    # Getter methods for cpu_average_method_delete
    def get_cpu_average_method_delete(self):
        return self.cpu_average_method_delete

    # Getter methods for ram_average_method_delete
    def get_ram_average_method_delete(self):
        return self.ram_average_method_delete

    # Getter methods for bw_average_method_delete
    def get_bw_average_method_delete(self):
        return self.bw_average_method_delete

    def create_batch(self, batch_size):
        batch = [
            {'method': 'GET', 'endpoint': 'get'},
            {'method': 'POST', 'endpoint': 'post', 'payload': {'key': 'value'}},
            {'method': 'DELETE', 'endpoint': 'delete'},
            {'method': 'PUT', 'endpoint': 'put', 'payload': {'key': 'value'}},
        ]
        return [random.choice(batch) for _ in range(batch_size)]

    def create_load(self, request_num, batches_num, sleep_time=True,load_type='normal'):
        # Batch init
        self.cpu_each_batch=[]
        self.ram_each_batch=[]
        self.bw_each_batch=[]

        # Request init
        self.cpu_each_request=[]
        self.ram_each_request=[]
        self.bw_each_request=[]
        cpu_per_batch_means=[]
        ram_per_batch_means=[]
        bw_per_batch_means=[]

        # post init
        cpu_sum_method_post=0
        ram_sum_method_post=0
        bw_sum_method_post=0
        post_count=0

        # get init
        cpu_sum_method_get=0
        ram_sum_method_get=0
        bw_sum_method_get=0
        get_count=0

        # put init
        cpu_sum_method_put=0
        ram_sum_method_put=0
        bw_sum_method_put=0
        put_count=0

        # delete init
        cpu_sum_method_delete=0
        ram_sum_method_delete=0
        bw_sum_method_delete=0
        delete_count=0

        print(f"{load_type}------------------------------------------")

        response_times = []
        futures = []
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
                    cpu,ram,bw,request_response_time=future.result()
                    # print("::::",cpu,ram,bw)
                    self.cpu_each_request.append(cpu)
                    self.ram_each_request.append(ram)
                    self.bw_each_request.append(bw)
                    response_times.append(request_response_time)
                    cpu_batch_sum+=cpu
                    ram_batch_sum+=ram
                    bw_batch_sum+=bw
                    if request['method']=='POST':
                        cpu_sum_method_post+=cpu
                        ram_sum_method_post+=ram
                        bw_sum_method_post+=bw
                        post_count+=1
                    if request['method']=='GET':
                        cpu_sum_method_get+=cpu
                        ram_sum_method_get+=ram
                        bw_sum_method_get+=bw
                        get_count+=1
                    if request['method']=='PUT':
                        cpu_sum_method_put+=cpu
                        ram_sum_method_put+=ram
                        bw_sum_method_put+=bw
                        put_count+=1
                    if request['method']=='DELETE':
                        cpu_sum_method_delete+=cpu
                        ram_sum_method_delete+=ram
                        bw_sum_method_delete+=bw
                        delete_count+=1
            cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            ram_per_batch_means.append(ram_batch_sum/batch_size)
            bw_per_batch_means.append(bw_batch_sum/batch_size)
            self.cpu_each_batch.append(cpu_batch_sum)
            self.ram_each_batch.append(ram_batch_sum)
            self.bw_each_batch.append(bw_batch_sum)
            if sleep_time:
                time.sleep(1)  # Adjust sleep time as needed
        if post_count==0:
            post_count=1
        if get_count==0:
            get_count=1
        if put_count==0:
            put_count=1
        if delete_count==0:
            delete_count=1

        self.cpu_average_method_post=cpu_sum_method_post/post_count
        self.ram_average_method_post=ram_sum_method_post/post_count
        self.bw_average_method_post=bw_sum_method_post/post_count
        self.cpu_average_method_get=cpu_sum_method_get/get_count
        self.ram_average_method_get=ram_sum_method_get/get_count
        self.bw_average_method_get=bw_sum_method_get/get_count
        self.cpu_average_method_put=cpu_sum_method_put/put_count
        self.ram_average_method_put=ram_sum_method_put/put_count
        self.bw_average_method_put=bw_sum_method_put/put_count
        self.cpu_average_method_delete=cpu_sum_method_delete/delete_count
        self.ram_average_method_delete=ram_sum_method_delete/delete_count
        self.bw_average_method_delete=bw_sum_method_delete/delete_count

        # self.printResults(cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means,response_times)
        return futures

    def printResults(self,cpu_per_batch_means,ram_per_batch_means,bw_per_batch_means,response_time_list):
        print(f'Average CPU per batch:{cpu_per_batch_means}')
        print(f'Average RAM per batch:{ram_per_batch_means}')
        print(f'Average BW per batch:{bw_per_batch_means}')

        print(f'Average CPU of load: {sum(cpu_per_batch_means)/len(cpu_per_batch_means)}')
        print(f'Average RAM of load: {sum(ram_per_batch_means)/len(ram_per_batch_means)}')
        print(f'Average BW of load: {sum(bw_per_batch_means)/len(bw_per_batch_means)}\n')
        print(f'Average Response time of load: {sum(response_time_list)/len(response_time_list)}\n')

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



lock = threading.Lock()
# returns per request the total->CPU,RAM,BW,response time
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

    # with lock:
    #     response_times.append(response_time)

    # print(f"Request {method} {endpoint}:\nStatus Code: {response.status_code}\nResponse Time: {response_time} (sec)\nCPU: {mon_obj.cpu_util} (%)\nRAM: {mon_obj.ram_util} (%)\nBandwidth: {mon_obj.bw_util} (bits/sec)")

    return sum(mon_obj.cpu_util),sum(mon_obj.ram_util),sum(mon_obj.bw_util),response_time
