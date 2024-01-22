from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from BasicMonitoring import Monitoring
import requests
import time
import random
import psutil
import threading

NUMBER_OF_BATCHES = 5
MAXIMUM_BATCH_SIZE = 5
MINIMUM_BATCH_SIZE = 1

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

    # Start monitoring CPU usage
    mon_obj.event.clear()
    monitoring_thread = threading.Thread(target=mon_obj.monitor_cpu)
    monitoring_thread.start()

    # Make a request
    start_time = time.time()
    response = create_request(endpoint, method, payload)
    end_time = time.time()

    # Stop monitoring after the request is made
    mon_obj.event.set()
    monitoring_thread.join()  # Wait for the monitoring thread to finish

    # Process the response (you can customize this based on your needs)
    response_time = end_time - start_time

    # Use a lock to protect shared resource
    with lock:
        response_times.append(response_time)

    print(f"Request {method} {endpoint} - Status Code: {response.status_code} - Response Time: {response_time} seconds - CPU: {mon_obj.cpu_util}")

event = threading.Event()
mon_obj = Monitoring([], [], event)

with ThreadPoolExecutor() as executor:
    futures = []

    for i in range(NUMBER_OF_BATCHES):
        print(f"\nBatch Number: {i}")
        batch_size = random.randint(MINIMUM_BATCH_SIZE, MAXIMUM_BATCH_SIZE)

        batch = [
            {'method': 'GET', 'endpoint': 'get'},
            {'method': 'POST', 'endpoint': 'post', 'payload': {'key': 'value'}},
            {'method': 'DELETE', 'endpoint': 'delete'},
            {'method': 'PUT', 'endpoint': 'put', 'payload': {'key': 'value'}},
        ]

        for _ in range(batch_size):
            # print('new request')
            request = random.choice(batch)
            future = executor.submit(run_request_with_monitoring, request, mon_obj)
            futures.append(future)

    # Wait for all futures to complete without blocking the main thread
    done, _ = wait(futures, return_when=FIRST_COMPLETED)
    for future in done:
        future.result()

print(f'\nTail latency: {max(response_times):.6f} seconds')
response_times.sort(reverse=True)
print("\nResponse Times (sorted):", response_times)
tail_latency = response_times[int(0.99 * len(response_times))]
print(f"\nTail Latency (99th percentile): {tail_latency:.6f} seconds")
