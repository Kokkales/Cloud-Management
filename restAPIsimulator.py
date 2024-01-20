import requests
import time
import random

NUMBER_OF_BATCHES=5
MAXIMUM_BATCH_SIZE=5
MINIMUM_BATCH_SIZE=1

def createRequest(endpoint,method,payload):
    url=f"http://localhost:5000/{endpoint}"
    headers={'Content-Type':'application/json'}
    if method=='GET':
        resp=requests.get(url,headers=headers)
    elif method=='POST':
        resp=requests.post(url,headers=headers,json=payload)
    elif method=='DELETE':
        resp=requests.delete(url,headers=headers)
    elif method=='PUT':
        resp=requests.put(url,headers=headers,json=payload)
    return resp

for i in range(NUMBER_OF_BATCHES):  # Number of batches
    print(f"\nBatch Number: {i}")
    batch_size = random.randint(MINIMUM_BATCH_SIZE,MAXIMUM_BATCH_SIZE)  # Random batch size
    # frequency = random.uniform(1, 5)  # Random frequency (sleep duration)

    # Generate a batch of requests
    batch = [
        {'method': 'GET', 'endpoint': 'get'},
        {'method': 'POST', 'endpoint': 'post', 'payload': {'key': 'value'}},
        {'method': 'DELETE', 'endpoint': 'delete'},
        {'method': 'PUT', 'endpoint': 'put', 'payload': {'key': 'value'}},
    ]

    for _ in range(batch_size):
        request = random.choice(batch)
        method = request['method']
        endpoint = request['endpoint']
        payload = request.get('payload')

        # Make a request
        response = createRequest(endpoint, method, payload)

        # Process the response (you can customize this based on your needs)
        print(f"Request {method} {endpoint} - Status Code: {response.status_code}")

    # Sleep to simulate different frequencies between batches
    # time.sleep(frequency)
