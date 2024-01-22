import time
import psutil
import csv
import pickle
import numpy as np
from scipy import stats
import statistics
import random
import matplotlib.pyplot as plt
import os

class BasicMonitoring:
  def __init__(self, cpu_util, ram_util):
    self.__cpu_util = cpu_util
    self.__ram_util = ram_util

  def set_cpu_util(self, cpu_util):
    self.__cpu_util = cpu_util

  def get_cpu_util(self):
    return self.__cpu_util

  def set_ram_util(self, ram_util):
    self.__ram_util = ram_util

  def get_ram_util(self):
    return self.__ram_util

class Monitoring(BasicMonitoring):
  __num_obj=0
  def __init__(self, cpu_util, ram_util, event):
    Monitoring.__num_obj += 1
    self.cpu_util = cpu_util
    self.ram_util = ram_util
    self._timestamp = time.time()
    self.event = event  # Event to signal the end of CPU monitoring

  def __call__(self):
    print ("CPU utilization: " + str(self.cpu_util))
    print ("RAM utilization: " + str(self.ram_util))

  @staticmethod
  def get_system_info():
    print("Number of CPUs: %s" % ( psutil.cpu_count()))
    print("Total Ram: {} ".format(psutil.virtual_memory()[0]))
    print("Disk size: " + str(psutil.disk_usage('/')[0]))

  @classmethod
  def get_num_obj(cls):
    return cls.__num_obj

#   def monitor_cpu(self, num_steps, time_step=1):
#     for i in range(num_steps):
#         if self.event.is_set():
#             break  # Stop monitoring if the event is set
#         self.cpu_util.append(psutil.cpu_percent(interval=None))
#         time.sleep(time_step)
  def monitor_cpu(self, time_step=1):
    while not self.event.is_set():
        self.cpu_util.append(psutil.cpu_percent(interval=None))
        # self.cpu_util.append(os.cpu_percent(interval=None))
        time.sleep(time_step)

  def monitor_ram(self,time_step=1):
    while not self.event.is_set():
        self.ram_util.append(psutil.virtual_memory().percent)
        time.sleep(time_step)

  def get_timestamp(self):
    print(time.ctime(self._timestamp))

  def save_cpu_ram(self, filepath):
    all_metrics=[]
    for cpu, ram in zip(self.cpu_util, self.ram_util):
      two_metrics=[]
      two_metrics.append(cpu)
      two_metrics.append(ram)
      all_metrics.append(two_metrics)
      print(two_metrics)

    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(self.cpu_util, self.ram_util))

  def save_monitoring(self, filepath):
    pickle.dump(self, open(filepath, "wb" ))

  def descriptive_statistics(self, metric):
    if metric.lower()=="cpu":
      data=self.cpu_util
    elif metric.lower()=="ram":
      data=self.ram_util
    else:
      print("Wrong input. Type cpu or ram.")
      return
    print ("Min: "+str(stats.describe(data)[1][0]))
    print ("Max: "+str(stats.describe(data)[1][1]))
    print ("Average: " + str(statistics.mean(data)))
    print ("Median (middle value): " + str(statistics.median(data)))
    try:
      print ("Mode (most common value): " + str(statistics.mode(data)))
    except:
      print ("A random value: " + str(random.choice(data)))
    print ("Standard Deviation: "+ str(statistics.stdev(data)))

  @staticmethod
  def load_monitoring(filepath):
    return pickle.load(open(filepath, "rb" ))

class VizualizeMonitoring (Monitoring):
  def __call__(self):
      data=self.cpu_util
      maximum = lambda a,b:a if a > b else b
      plt.plot(range(1, len(data)+1), data, label='CPU') #range(maximum(len(self.cpu_util), len(self.ram_util))+1)
      data=self.ram_util
      plt.plot(range(1,len(data)+1), data, label='RAM')
      plt.legend()
      plt.xlabel("timesteps")
      plt.ylabel("utilization")
      plt.show()