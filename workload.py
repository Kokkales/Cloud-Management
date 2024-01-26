from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from BasicMonitoring import Monitoring
import requests
import time
import random
import psutil
import threading

class WorkloadCreator():
    def __init__(self,cpu_each_batch=[],ram_each_batch=[],bw_each_batch=[],cpu_each_request=[],ram_each_request=[],bw_each_request=[],cpu_average_method_post=0,ram_average_method_post=0,bw_average_method_post=0,cpu_average_method_get=0,ram_average_method_get=0,bw_average_method_get=0,cpu_average_method_put=0,ram_average_method_put=0,bw_average_method_put=0,cpu_average_method_delete=0,ram_average_method_delete=0,bw_average_method_delete=0,response_times=[],batches_num=5,request_num=10,sleep_time=0,timestamp=None):
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

        self.response_times=response_times

        self.batches_num=batches_num
        self.request_num=request_num
        self.sleep_time=sleep_time
        self.timestamp=timestamp

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

    def get_batches_number(self):
        return self.batches_num

    def get_request_number(self):
        return self.request_num

    def get_response_times(self):
        return self.response_times

    def get_timestamp(self):
        self.timestamp=time.ctime(time.time())
        return self.timestamp

    def create_batch(self, batch_size):
        batch = [
            {'method': 'GET', 'endpoint': 'get'},
            {'method': 'POST', 'endpoint': 'post', 'payload': {'key': 'value'}},
            {'method': 'DELETE', 'endpoint': 'delete'},
            {'method': 'PUT', 'endpoint': 'put', 'payload': {'key': 'value'}},
        ]
        return [random.choice(batch) for _ in range(batch_size)]

    def create_load(self,load_type='normal'):
        # self.__init__()
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

        self.response_times = []

        print(f"{load_type}------------------------------------------")

        futures = []
        batch_size_sum=0
        new_req_num=self.request_num
        for i in range(self.batches_num):
            # stats
            cpu_batch_sum=0
            ram_batch_sum=0
            bw_batch_sum=0
            response_times_sum=0

            if load_type=='stable':
                batch_size = self.request_num // self.batches_num
                remaining_requests = self.request_num % self.batches_num
                if i < remaining_requests:
                    current_batch_size = batch_size + 1
                else:
                    current_batch_size = batch_size
                batch_size=current_batch_size
            elif load_type=='normal':
                remaining_requests = self.request_num - i
                max_batch_size = remaining_requests // (self.batches_num - i)

                if i == self.batches_num - 1:
                    # If it's the last batch, include all remaining requests
                    batch_size = remaining_requests
                else:
                    current_batch_size = random.randint(1, max_batch_size)
                    batch_size = current_batch_size
            elif load_type=='peak': #TODO
                batch_size = self.request_num // self.batches_num
            else: #TODO
                batch_size = self.request_num // self.batches_num

                if i == random.randint(1,9):
                    batch_size *= 3  # Triple the requests in the spike batch

            batch = self.create_batch(batch_size)
            print(batch_size)
            for k in range(batch_size):
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
                    response_times_sum+=request_response_time
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
            # cpu_per_batch_means.append(cpu_batch_sum/batch_size)
            # ram_per_batch_means.append(ram_batch_sum/batch_size)
            # bw_per_batch_means.append(bw_batch_sum/batch_size)
            self.cpu_each_batch.append(cpu_batch_sum/batch_size)
            self.ram_each_batch.append(ram_batch_sum/batch_size)
            self.bw_each_batch.append(bw_batch_sum/batch_size)
            self.response_times.append(response_times_sum)
            if self.sleep_time==-1:
                time.sleep(random.int(1,5))  # Sleep time between each batch
            elif self.sleep_time!=0:
                time.sleep(self.sleep_time)
            else:
                continue
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
# returns per request the average->CPU,RAM,BW,response time
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

    return sum(mon_obj.cpu_util)/len(mon_obj.cpu_util),sum(mon_obj.ram_util)/len(mon_obj.ram_util),sum(mon_obj.bw_util)/len(mon_obj.bw_util),response_time
