from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from workload import WorkloadCreator
from plotter import Plotter
import re
import ast
import json

# Function to print results to a file
def printResultsToFile(file_path,type,id=[0]):
    with open(file_path, 'w') as file:
        file.write('&')
        file.write(f'ID: {id[0]+1}')
        file.write(f'Load Type: {type}')
        file.write(f'Timestamp: {workload_creator.get_timestamp()}\n')
        file.write(f"Concept\nRequests Number:{workload_creator.get_request_number()}\nBatches Number:{workload_creator.get_batches_number()}\nSleep time:{workload_creator.sleep_time}\n")
        file.write('-------BATCH-------\n')
        file.write(f'BATCH CPU: {workload_creator.get_cpu_each_batch()}\n')
        file.write(f'BATCH RAM: {workload_creator.get_ram_each_batch()}\n')
        file.write(f'BATCH BW: {workload_creator.get_bw_each_batch()}\n')
        file.write('-------REQUESTS-------\n')
        file.write(f'REQUEST CPU: {workload_creator.get_cpu_each_request()}\n')
        file.write(f'REQUEST RAM: {workload_creator.get_ram_each_request()}\n')
        file.write(f'REQUEST BW: {workload_creator.get_bw_each_request()}\n')
        file.write('-------POST REQUEST-------\n')
        file.write(f'POST Avg CPU: {workload_creator.get_cpu_average_method_post()}\n')
        file.write(f'POST Avg RAM: {workload_creator.get_ram_average_method_post()}\n')
        file.write(f'POST Avg BW: {workload_creator.get_bw_average_method_post()}\n')
        file.write('-------GET REQUEST-------\n')
        file.write(f'GET Avg CPU: {workload_creator.get_cpu_average_method_get()}\n')
        file.write(f'GET Avg RAM: {workload_creator.get_ram_average_method_get()}\n')
        file.write(f'GET Avg BW: {workload_creator.get_bw_average_method_get()}\n')
        file.write('-------PUT REQUEST-------\n')
        file.write(f'PUT Avg CPU: {workload_creator.get_cpu_average_method_put()}\n')
        file.write(f'PUT Avg RAM: {workload_creator.get_ram_average_method_put()}\n')
        file.write(f'PUT Avg BW: {workload_creator.get_bw_average_method_put()}\n')
        file.write('-------DELETE REQUEST-------\n')
        file.write(f'DELETE Avg CPU: {workload_creator.get_cpu_average_method_delete()}\n')
        file.write(f'DELETE Avg RAM: {workload_creator.get_ram_average_method_delete()}\n')
        file.write(f'DELETE Avg BW: {workload_creator.get_bw_average_method_delete()}\n\n')
        file.write(f'Response Time:: {workload_creator.get_response_times()}\n\n')
        file.write('\n\n')
        # visualiser.plot_cpu_ram_bw(workload_creator.get_cpu_each_batch(), workload_creator.get_ram_each_batch(), workload_creator.get_bw_each_batch(), type='batches')
        # visualiser.plot_cpu_ram_bw(workload_creator.get_cpu_each_request(), workload_creator.get_ram_each_request(), workload_creator.get_bw_each_request(), type='request')
        # visualiser.plot_request_types_usage(workload_creator.get_cpu_average_method_post(), workload_creator.get_cpu_average_method_get(), workload_creator.get_cpu_average_method_put(), workload_creator.get_cpu_average_method_delete(), workload_creator.get_ram_average_method_post(), workload_creator.get_ram_average_method_get(), workload_creator.get_ram_average_method_put(), workload_creator.get_ram_average_method_delete())
        # visualiser.plot_latency(2, 3)

def visualize_results_from_file(file_path,method):
    with open(file_path, 'r') as file:
        content = file.read()
        last_ampersand_index = content.rfind('&')

        # Set the file position to the last '&' if it exists, or the beginning otherwise
        file.seek(last_ampersand_index + 1 if last_ampersand_index != -1 else 0)

        # Now you can continue reading the content from the current file position
        content = file.read()

        # Extract data using regular expressions
        timestamp_match = re.search(r'Timestamp: (.+)', content)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
            print(f'Timestamp: {timestamp}')

        requests_match = re.search(r'Requests Number:(\d+)', content)
        batches_match = re.search(r'Batches Number:(\d+)', content)
        sleep_time_match = re.search(r'Sleep time:(\S+)', content)
        if requests_match and batches_match and sleep_time_match:
            requests_number = int(requests_match.group(1))
            batches_number = int(batches_match.group(1))
            sleep_time = sleep_time_match.group(1)
            print(f"Concept\nRequests Number: {requests_number}\nBatches Number: {batches_number}\nSleep time: {sleep_time}")

        # Extract and visualize other data as needed
        batch_cpu_match = re.search(r'BATCH CPU: (.+)', content)
        if batch_cpu_match:
            batch_cpu_data =ast.literal_eval(batch_cpu_match.group(1))
            print(f'BATCH CPU Data: {batch_cpu_data}')
        batch_ram_match = re.search(r'BATCH RAM: (.+)', content)
        if batch_ram_match:
            batch_ram_data =ast.literal_eval(batch_ram_match.group(1))
            print(f'BATCH RAM Data: {batch_ram_data}')

        batch_bw_match = re.search(r'BATCH BW: (.+)', content)
        if batch_bw_match:
            batch_bw_data =ast.literal_eval(batch_bw_match.group(1))
            print(f'BATCH BW Data: {batch_bw_data}')

        requests_cpu_match = re.search(r'REQUEST CPU: (.+)', content)
        if requests_cpu_match:
            requests_cpu_data =ast.literal_eval(requests_cpu_match.group(1))
            print(f'REQUESTS CPU Data: {requests_cpu_data}')

        requests_ram_match = re.search(r'REQUEST RAM: (.+)', content)
        if requests_ram_match:
            requests_ram_data =ast.literal_eval(requests_ram_match.group(1))
            print(f'REQUESTS RAM Data: {requests_ram_data}')

        requests_bw_match = re.search(r'REQUEST BW: (.+)', content)
        if requests_bw_match:
            requests_bw_data =ast.literal_eval(requests_bw_match.group(1))
            print(f'REQUESTS BW Data: {requests_bw_data}')

        avg_post_cpu_match = re.search(r'POST Avg CPU: (.+)', content)
        if avg_post_cpu_match:
            avg_post_cpu_data =ast.literal_eval(avg_post_cpu_match.group(1))
            print(f'Avg POST CPU Data: {avg_post_cpu_data}')

        avg_post_ram_match = re.search(r'POST Avg RAM: (.+)', content)
        if avg_post_ram_match:
            avg_post_ram_data =ast.literal_eval(avg_post_ram_match.group(1))
            print(f'Avg POST RAM Data: {avg_post_ram_data}')

        avg_post_bw_match = re.search(r'POST Avg BW: (.+)', content)
        if avg_post_bw_match:
            avg_post_bw_data =ast.literal_eval(avg_post_bw_match.group(1))
            print(f'Avg POST BW Data: {avg_post_bw_data}')

        avg_get_cpu_match = re.search(r'GET Avg CPU: (.+)', content)
        if avg_get_cpu_match:
            avg_get_cpu_data =ast.literal_eval(avg_get_cpu_match.group(1))
            print(f'Avg GET CPU Data: {avg_get_cpu_data}')

        avg_get_ram_match = re.search(r'GET Avg RAM: (.+)', content)
        if avg_get_ram_match:
            avg_get_ram_data =ast.literal_eval(avg_get_ram_match.group(1))
            print(f'Avg GET RAM Data: {avg_get_ram_data}')

        avg_get_bw_match = re.search(r'GET Avg BW: (.+)', content)
        if avg_get_bw_match:
            avg_get_bw_data =ast.literal_eval(avg_get_bw_match.group(1))
            print(f'Avg GET BW Data: {avg_get_bw_data}')

        avg_put_cpu_match = re.search(r'PUT Avg CPU: (.+)', content)
        if avg_put_cpu_match:
            avg_put_cpu_data =ast.literal_eval(avg_put_cpu_match.group(1))
            print(f'Avg PUT CPU Data: {avg_put_cpu_data}')

        avg_put_ram_match = re.search(r'PUT Avg RAM: (.+)', content)
        if avg_put_ram_match:
            avg_put_ram_data =ast.literal_eval(avg_put_ram_match.group(1))
            print(f'Avg PUT RAM Data: {avg_put_ram_data}')

        avg_put_bw_match = re.search(r'PUT Avg BW: (.+)', content)
        if avg_put_bw_match:
            avg_put_bw_data =ast.literal_eval(avg_put_bw_match.group(1))
            print(f'Avg PUT BW Data: {avg_put_bw_data}')

        avg_delete_cpu_match = re.search(r'DELETE Avg CPU: (.+)', content)
        if avg_delete_cpu_match:
            avg_delete_cpu_data =ast.literal_eval(avg_delete_cpu_match.group(1))
            print(f'Avg DELETE CPU Data: {avg_delete_cpu_data}')

        avg_delete_ram_match = re.search(r'DELETE Avg RAM: (.+)', content)
        if avg_delete_ram_match:
            avg_delete_ram_data =ast.literal_eval(avg_delete_ram_match.group(1))
            print(f'Avg DELETE RAM Data: {avg_delete_ram_data}')

        avg_delete_bw_match = re.search(r'DELETE Avg BW: (.+)', content)
        if avg_delete_bw_match:
            avg_delete_bw_data =ast.literal_eval(avg_delete_bw_match.group(1))
            print(f'Avg DELETE BW Data: {avg_delete_bw_data}')

        response_time_match = re.search(r'Response Time:: (.+)', content)
        if response_time_match:
            response_time_data =ast.literal_eval(response_time_match.group(1))
            print(f'Response Time Data: {response_time_data}')

        # Visualize data
        if batch_cpu_data and batch_ram_data and batch_bw_data:
            visualiser.plot_cpu_ram_bw(batch_cpu_data, batch_ram_data, batch_bw_data, type='batches',method=method)
            visualiser.plot_cpu_ram_bw(requests_cpu_data, requests_ram_data,requests_bw_data, type='request',method=method)
            visualiser.plot_request_types_usage(avg_post_cpu_data, avg_get_cpu_data, avg_put_cpu_data, avg_delete_cpu_data, avg_post_ram_data, avg_get_ram_data, avg_put_ram_data, avg_delete_ram_data,method=method)
            # visualiser.plot_latency(2, 3)

# Set the file path
file_path = 'simulatorResults.txt'

workload_creator = WorkloadCreator(request_num=5, batches_num=3, sleep_time=0)  # -1 means random sleep time in each batch
visualiser = Plotter(request_num=workload_creator.get_request_number(), batches_num=workload_creator.get_batches_number(), sleep_time=0)

# Redirect prints to the file

# Stable Load
stable_futures = workload_creator.create_load(load_type='stable')
wait(stable_futures, return_when=FIRST_COMPLETED)
printResultsToFile(file_path,'Stable')
visualize_results_from_file(file_path,'Stable')

# Normal Load
normal_futures = workload_creator.create_load(load_type='normal')
wait(normal_futures, return_when=FIRST_COMPLETED)
printResultsToFile(file_path,'Normal')
visualize_results_from_file(file_path,'Normal')

# Peak Load
peak_futures = workload_creator.create_load(load_type='peak')
wait(peak_futures, return_when=FIRST_COMPLETED)
printResultsToFile(file_path,'Peak')
visualize_results_from_file(file_path,'Peak')

# # Spike Load
# spike_futures = workload_creator.create_load(load_type='spike')
# wait(spike_futures, return_when=FIRST_COMPLETED)
# printResultsToFile(file_path)
