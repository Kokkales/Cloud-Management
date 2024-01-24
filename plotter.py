import numpy as np
import matplotlib.pyplot as plt

class Plotter:

    def __init__(self,request_num=10,batches_num=5,sleep_time=0):
        self.request_num=request_num
        self.batches_num=batches_num
        self.sleep_time=sleep_time

    def plot_batch_oriented(self,cpu_values,ram_values,bw_values):
        batch_numbers = list(range(1,self.batches_num + 1))

        # Plotting CPU
        plt.plot(batch_numbers,cpu_values, marker='o', label='CPU')
        # Plotting RAM
        plt.plot(batch_numbers,ram_values, marker='o', label='RAM')
        # Plotting BW
        plt.plot(batch_numbers,bw_values, marker='o', label='BW')

        plt.title('Performance Metrics Over Batches')
        plt.xlabel('Batch Number')
        plt.ylabel('Usage')
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_request_oriented():
        return

    def plot_time_oriented():
        return