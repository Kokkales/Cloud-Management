import requests
import random

class WorkloadCreator():
    def __init__(self,load):
        self.load=load

    # Stable Load
    def create_stable_load(self,request_num,batches_num,sleep_time=True):
        # Create a number of requests
        # seperate the requests into same size batches
        # set sleep time per batch
        return

    # Normal Load
    def create_normal_load(self):
        # Create a number of requests
        # seperate the requests into random size batches
        # set sleep time per batch
        return

    # Peak Load
    def create_peak_load(self):
        # Create a number of requests
        # seperate the requests into random size batches
        # in one random batch triple the requests
        # set sleep time per batch
        return

    # Spike Load
    def create_spike_load(self):
        # Create a number of requests
        # seperate the requests into random size batches
        # in one random batch triple the requests
        # set sleep time per batch
        return

    # # Data Volume Load
    # def create_data_volume_load(self):
    #     return

    # Stress Load - EXTRA
    def create_stress_load(self):
        return