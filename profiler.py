import psutil
import pandas 
import time
from tqdm import tqdm
import sys
from matplotlib import pyplot

cpu_usage = []
ram_usage = []
bytes_sent = []
bytes_recv = []

profiling_time = 10
interval =  1

args = ""

try:
    args = str(sys.argv[3])
except:
    args = "-crdu"


profilerFilter = []


if(args.startswith("-")):
    if "c" in args:
        profilerFilter.append("CPU%")
    if "r" in args:
        profilerFilter.append("RAM%")
    if "d" in args:
        profilerFilter.append("Download (mbit/s)")
    if "u" in args:
        profilerFilter.append("Upload (mbit/s)")

try:
    profiling_time = int(sys.argv[1])
except:
    profiling_time = 10


try:
    interval = float(sys.argv[2])
except:
    interval = 1
    

for i in tqdm(range(profiling_time)):

    data_before = psutil.net_io_counters()

    cpu_usage.append(psutil.cpu_percent())
    ram_usage.append(psutil.virtual_memory().percent)

    time.sleep(interval)
    data_after = psutil.net_io_counters()
    
    bytes_sent.append(data_after.bytes_sent / 125000 - data_before.bytes_sent / 125000)
    bytes_recv.append(data_after.bytes_recv / 125000 - data_before.bytes_recv / 125000)


data = {

    "CPU%" : cpu_usage,
    "RAM%" : ram_usage,
    "Download (mbit/s)" : bytes_recv,
    "Upload (mbit/s)" : bytes_sent

}

df = pandas.DataFrame(data)

print(df[profilerFilter])

df[profilerFilter].plot(kind="line")
pyplot.show()