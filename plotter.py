import numpy as np
import matplotlib.pyplot as plt


def normalize(value, min_value, max_value):
    new_value=[]
    for item in value:
        new_value.append((item - min_value) / (max_value - min_value))
    return new_value

class Plotter:

    def __init__(self,sleep_time=0):
        self.sleep_time=sleep_time

    def plot_cpu_ram_bw(self,folder_path,cpu_values,ram_values,bw_values,type='batches',method='normal'):
        if type == 'batches':
            # batch_numbers = list(range(1, self.batches_num + 1))
            batch_numbers = list(range(1, len(cpu_values) + 1))
            x_label='Batch Number'
        else:
            # batch_numbers = list(range(1,self.request_num + 1))
            batch_numbers = list(range(1, len(cpu_values) + 1))
            x_label='Request Number'
        bw_values = normalize(bw_values, 0, 1000)  # Adjust the max value based on your expected bandwidth
        cpu_values = normalize(cpu_values, 0, 100)
        ram_values = normalize(ram_values, 0, 100)

        # Create a 1x2 grid of subplots
        plt.figure('1')
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Plotting CPU and RAM on the first subplot
        axs[0].plot(batch_numbers, cpu_values, marker='o', label='CPU')
        axs[0].plot(batch_numbers, ram_values, marker='o', label='RAM')
        axs[0].set_title('CPU and RAM Usage Over Batches')
        axs[0].set_xlabel(x_label)
        axs[0].set_ylabel('Usage')
        axs[0].grid(True)
        axs[0].legend()

        # Plotting BW on the second subplot
        axs[1].plot(batch_numbers, bw_values, marker='o', label='BW')
        axs[1].set_title('Bandwidth Usage Over Batches')
        axs[1].set_xlabel(x_label)
        axs[1].set_ylabel('Usage')
        axs[1].grid(True)
        axs[1].legend()

        # Adjust layout to prevent clipping of titles
        plt.tight_layout()
        # Save the figure
        plt.savefig(f'{folder_path}{type}{method}.jpg')

        # Display the subplots
        # plt.show()

        return


    def plot_request_types_usage(self,folder_path,cpu_post_value,cpu_get_value,cpu_put_value,cpu_delete_value,ram_post_value,ram_get_value,ram_put_value,ram_delete_value,method):
        # Sample data
        categories = ['GET', 'POST', 'PUT', 'DELETE']
        values1 = [cpu_post_value,cpu_get_value,cpu_put_value,cpu_delete_value]
        values2 = [ram_post_value,ram_get_value,ram_put_value,ram_delete_value]

        # Width of the bars
        bar_width = 0.35

        # Set the positions of bars on X-axis
        r1 = np.arange(len(categories))
        r2 = [x + bar_width for x in r1]
        plt.figure('2')
        # Plotting the double bar chart
        plt.bar(categories, values1, color='blue', width=bar_width, edgecolor='grey', label='CPU')
        plt.bar(r2, values2, color='orange', width=bar_width, edgecolor='grey', label='RAM')

        # Adding labels and title
        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.title('CPU and RAM')

        # Adding legend
        plt.legend()
        # Save the figure
        plt.savefig(f'{folder_path}requestTypes{method}.jpg')

        # # Display the chart
        # plt.show()
        return

    def plot_final_results(self,folder_path,stable_response_times,stable_tail_latency,normal_response_times,normal_tail_latency,peak_response_times,peak_tail_latency):
        # Sample data for the table
        data = [
            ['Workload Type', 'Total Response Time','Average Response Time','Tail latency'],
            ['Stable', sum(stable_response_times), sum(stable_response_times)/len(stable_response_times),stable_tail_latency],
            ['Normal', sum(normal_response_times), sum(normal_response_times)/len(normal_response_times),normal_tail_latency],
            ['Peak', sum(peak_response_times),sum(peak_response_times)/len(peak_response_times),peak_tail_latency]
        ]

        # Create a figure and axis
        plt.figure('3', figsize=(30,10))
        fig, ax = plt.subplots(figsize=(10, 5))

        # Hide the axes
        ax.axis('off')

        # Plot the table
        table = ax.table(cellText=data, loc='center', cellLoc='center', colLabels=None)

        # Adjust the font size of the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)

        # Adjust the cell heights and widths
        table.scale(1, 1)

        # Save the figure
        plt.savefig('finalResultsTable.jpg')
        # Display the table
        # plt.show()
        return