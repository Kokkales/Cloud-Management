import psutil

print("The CPU usage is: ",psutil.cpu_percent(4)) #It calculates the percentage of CPU usage during that time frame.
print('RAM memory % used:', psutil.virtual_memory()[2])
print('RAM Used (GB):', psutil.virtual_memory()[3])
print('RAM Used (GB):', psutil.virtual_memory()[4])
print('RAM Used (GB):', psutil.virtual_memory()[1])
print('RAM Used (GB):', psutil.virtual_memory()[0])
import psutil
import time

def calculate_total_network_bandwidth(interval=1):
    # Get the initial network usage
    initial_stats = psutil.net_io_counters()

    # Wait for the specified interval
    time.sleep(interval)

    # Get the final network usage
    final_stats = psutil.net_io_counters()

    # Calculate the total bandwidth
    sent_bytes = final_stats.bytes_sent - initial_stats.bytes_sent
    received_bytes = final_stats.bytes_recv - initial_stats.bytes_recv

    # Convert bytes to bits and calculate the total bandwidth in bits per second
    total_bandwidth = (sent_bytes + received_bytes) * 8 / 1
    # total_bandwidth = (sent_bytes + received_bytes) /1024**2

    return total_bandwidth

# Example usage
total_bandwidth = calculate_total_network_bandwidth()

print(f"Total Bandwidth: {total_bandwidth:.2f} bits/s")
