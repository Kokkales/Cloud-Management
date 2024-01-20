import psutil

print("The CPU usage is: ",psutil.cpu_percent(4)) #It calculates the percentage of CPU usage during that time frame.
print('RAM memory % used:', psutil.virtual_memory()[2])
print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)