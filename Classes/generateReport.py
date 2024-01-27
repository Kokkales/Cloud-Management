import matplotlib.pyplot as plt
import re
import ast
from Classes.plotter import Plotter

class ReportGenerator:
    def __init__(self,folder_path):
        self.folder_path=folder_path

    def save_to_file(self,id,file_path,load_type, timestamp,request_number,batches_number,sleep_time,cpu_each_batch,ram_each_batch,bw_each_batch,cpu_each_request,ram_each_request,bw_each_request,cpu_average_method_post,ram_average_method_post,bw_average_method_post,cpu_average_method_get,ram_average_method_get,bw_average_method_get,cpu_average_method_put,ram_average_method_put,bw_average_method_put,cpu_average_method_delete,ram_average_method_delete,bw_average_method_delete,response_times,tail_latency):
        with open(file_path, 'w') as file:
            file.write('&')
            file.write(f'ID: {id}\n')
            file.write(f'Load Type: {load_type}\n')
            file.write(f'Timestamp: {timestamp}\n')
            file.write(f"Concept\nRequests Number:{request_number}\nBatches Number:{batches_number}\nSleep time:{sleep_time}\n")
            file.write('-------BATCH-------\n')
            file.write(f'BATCH CPU: {cpu_each_batch}\n')
            file.write(f'BATCH RAM: {ram_each_batch}\n')
            file.write(f'BATCH BW: {bw_each_batch}\n')
            file.write('-------REQUESTS-------\n')
            file.write(f'REQUEST CPU: {cpu_each_request}\n')
            file.write(f'REQUEST RAM: {ram_each_request}\n')
            file.write(f'REQUEST BW: {bw_each_request}\n')
            file.write('-------POST REQUEST-------\n')
            file.write(f'POST Avg CPU: {cpu_average_method_post}\n')
            file.write(f'POST Avg RAM: {ram_average_method_post}\n')
            file.write(f'POST Avg BW: {bw_average_method_post}\n')
            file.write('-------GET REQUEST-------\n')
            file.write(f'GET Avg CPU: {cpu_average_method_get}\n')
            file.write(f'GET Avg RAM: {ram_average_method_get}\n')
            file.write(f'GET Avg BW: {bw_average_method_get}\n')
            file.write('-------PUT REQUEST-------\n')
            file.write(f'PUT Avg CPU: {cpu_average_method_put}\n')
            file.write(f'PUT Avg RAM: {ram_average_method_put}\n')
            file.write(f'PUT Avg BW: {bw_average_method_put}\n')
            file.write('-------DELETE REQUEST-------\n')
            file.write(f'DELETE Avg CPU: {cpu_average_method_delete}\n')
            file.write(f'DELETE Avg RAM: {ram_average_method_delete}\n')
            file.write(f'DELETE Avg BW: {bw_average_method_delete}\n\n')
            file.write(f'Response Time:: {response_times}\n')
            file.write(f'Tail Latency:: {tail_latency}\n\n')
            file.write('\n\n')
        return

    def plot_diagrams(self,file_path,load_type,sleep_time):
        visualiser = Plotter(sleep_time=sleep_time)
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
                # print(f'Timestamp: {timestamp}')

            id_match = re.search(r'ID: (.+)', content)
            if id_match:
                id = id_match.group(1)
                # print(f'id: {id}')

            load_type_match = re.search(r'Load Type: (.+)', content)
            if load_type_match:
                load_type = load_type_match.group(1)
                # print(f'load_type: {load_type}')

            requests_match = re.search(r'Requests Number:(\d+)', content)
            batches_match = re.search(r'Batches Number:(\d+)', content)
            sleep_time_match = re.search(r'Sleep time:(\S+)', content)
            if requests_match and batches_match and sleep_time_match:
                requests_number = int(requests_match.group(1))
                batches_number = int(batches_match.group(1))
                sleep_time = sleep_time_match.group(1)
                # print(f"Concept\nRequests Number: {requests_number}\nBatches Number: {batches_number}\nSleep time: {sleep_time}")

            # Extract and visualize other data as needed
            batch_cpu_match = re.search(r'BATCH CPU: (.+)', content)
            if batch_cpu_match:
                batch_cpu_data =ast.literal_eval(batch_cpu_match.group(1))
                # print(f'BATCH CPU Data: {batch_cpu_data}')
            batch_ram_match = re.search(r'BATCH RAM: (.+)', content)
            if batch_ram_match:
                batch_ram_data =ast.literal_eval(batch_ram_match.group(1))
                # print(f'BATCH RAM Data: {batch_ram_data}')

            batch_bw_match = re.search(r'BATCH BW: (.+)', content)
            if batch_bw_match:
                batch_bw_data =ast.literal_eval(batch_bw_match.group(1))
                # print(f'BATCH BW Data: {batch_bw_data}')

            requests_cpu_match = re.search(r'REQUEST CPU: (.+)', content)
            if requests_cpu_match:
                requests_cpu_data =ast.literal_eval(requests_cpu_match.group(1))
                # print(f'REQUESTS CPU Data: {requests_cpu_data}')

            requests_ram_match = re.search(r'REQUEST RAM: (.+)', content)
            if requests_ram_match:
                requests_ram_data =ast.literal_eval(requests_ram_match.group(1))
                # print(f'REQUESTS RAM Data: {requests_ram_data}')

            requests_bw_match = re.search(r'REQUEST BW: (.+)', content)
            if requests_bw_match:
                requests_bw_data =ast.literal_eval(requests_bw_match.group(1))
                # print(f'REQUESTS BW Data: {requests_bw_data}')

            avg_post_cpu_match = re.search(r'POST Avg CPU: (.+)', content)
            if avg_post_cpu_match:
                avg_post_cpu_data =ast.literal_eval(avg_post_cpu_match.group(1))
                # print(f'Avg POST CPU Data: {avg_post_cpu_data}')

            avg_post_ram_match = re.search(r'POST Avg RAM: (.+)', content)
            if avg_post_ram_match:
                avg_post_ram_data =ast.literal_eval(avg_post_ram_match.group(1))
                # print(f'Avg POST RAM Data: {avg_post_ram_data}')

            avg_post_bw_match = re.search(r'POST Avg BW: (.+)', content)
            if avg_post_bw_match:
                avg_post_bw_data =ast.literal_eval(avg_post_bw_match.group(1))
                # print(f'Avg POST BW Data: {avg_post_bw_data}')

            avg_get_cpu_match = re.search(r'GET Avg CPU: (.+)', content)
            if avg_get_cpu_match:
                avg_get_cpu_data =ast.literal_eval(avg_get_cpu_match.group(1))
                # print(f'Avg GET CPU Data: {avg_get_cpu_data}')

            avg_get_ram_match = re.search(r'GET Avg RAM: (.+)', content)
            if avg_get_ram_match:
                avg_get_ram_data =ast.literal_eval(avg_get_ram_match.group(1))
                # print(f'Avg GET RAM Data: {avg_get_ram_data}')

            avg_get_bw_match = re.search(r'GET Avg BW: (.+)', content)
            if avg_get_bw_match:
                avg_get_bw_data =ast.literal_eval(avg_get_bw_match.group(1))
                # print(f'Avg GET BW Data: {avg_get_bw_data}')

            avg_put_cpu_match = re.search(r'PUT Avg CPU: (.+)', content)
            if avg_put_cpu_match:
                avg_put_cpu_data =ast.literal_eval(avg_put_cpu_match.group(1))
                # print(f'Avg PUT CPU Data: {avg_put_cpu_data}')

            avg_put_ram_match = re.search(r'PUT Avg RAM: (.+)', content)
            if avg_put_ram_match:
                avg_put_ram_data =ast.literal_eval(avg_put_ram_match.group(1))
                # print(f'Avg PUT RAM Data: {avg_put_ram_data}')

            avg_put_bw_match = re.search(r'PUT Avg BW: (.+)', content)
            if avg_put_bw_match:
                avg_put_bw_data =ast.literal_eval(avg_put_bw_match.group(1))
                # print(f'Avg PUT BW Data: {avg_put_bw_data}')

            avg_delete_cpu_match = re.search(r'DELETE Avg CPU: (.+)', content)
            if avg_delete_cpu_match:
                avg_delete_cpu_data =ast.literal_eval(avg_delete_cpu_match.group(1))
                # print(f'Avg DELETE CPU Data: {avg_delete_cpu_data}')

            avg_delete_ram_match = re.search(r'DELETE Avg RAM: (.+)', content)
            if avg_delete_ram_match:
                avg_delete_ram_data =ast.literal_eval(avg_delete_ram_match.group(1))
                # print(f'Avg DELETE RAM Data: {avg_delete_ram_data}')

            avg_delete_bw_match = re.search(r'DELETE Avg BW: (.+)', content)
            if avg_delete_bw_match:
                avg_delete_bw_data =ast.literal_eval(avg_delete_bw_match.group(1))
                # print(f'Avg DELETE BW Data: {avg_delete_bw_data}')

            response_time_match = re.search(r'Response Time:: (.+)', content)
            if response_time_match:
                response_time_data =ast.literal_eval(response_time_match.group(1))
                # print(f'Response Time Data: {response_time_data}')

            tail_latency_match = re.search(r'Tail Latency:: (.+)', content)
            if tail_latency_match:
                tail_latency_data =ast.literal_eval(tail_latency_match.group(1))
                # print(f'Tail Latency Data: {tail_latency_data}')

            # Visualize data
            if batch_cpu_data and batch_ram_data and batch_bw_data:
                visualiser.plot_cpu_ram_bw(self.folder_path,batch_cpu_data, batch_ram_data, batch_bw_data, type='batches',method=load_type)
                visualiser.plot_cpu_ram_bw(self.folder_path,requests_cpu_data, requests_ram_data,requests_bw_data, type='request',method=load_type)
                visualiser.plot_request_types_usage(self.folder_path,avg_post_cpu_data, avg_get_cpu_data, avg_put_cpu_data, avg_delete_cpu_data, avg_post_ram_data, avg_get_ram_data, avg_put_ram_data, avg_delete_ram_data,method=load_type)
        return


    def plot_table(self,stable_response_times,stable_tail_latency,normal_response_times,normal_tail_latency,peak_response_times,peak_tail_latency,sleep_time):
        visualiser = Plotter(sleep_time=sleep_time)
        visualiser.plot_final_results(self.folder_path,stable_response_times,stable_tail_latency,normal_response_times,normal_tail_latency,peak_response_times,peak_tail_latency)
        return