import psutil
import platform
import GPUtil
from datetime import datetime

print("-"*40, "Sysinfo", "-"*40)
print("\n")
uname = platform.uname();

print(f"Dein System (es gibt nur Windows oder Unix based!) ist: {uname.system} based")
print(f"Dem Gerät sein krass Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
#print(f"bit: {uname.machine}")
print(f"Prozessor: {uname.processor}")
print('\n')

print("-"*39, "Start Zeit", "-"*39)
print('\n')
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Dem Gerät wurde am: {bt.day}.{bt.month}.{bt.year} um {bt.hour}:{bt.minute}:{bt.second} Uhr gebootet.")

print('\n')
print("-"*40, "CPU Info", "-"*40)
print('\n')

print("Echte Kerne:", psutil.cpu_count(logical=False))
print("Logische Kerne:", psutil.cpu_count(logical=True))
print(f"Max. Frequenz:, {psutil.cpu_freq().max:.1f}Mhz")
print(f"Aktuelle Frequenz:, {psutil.cpu_freq().current:.1f}Mhz")
print(f"CPU Auslastung:, {psutil.cpu_percent()}%")
print("CPU Auslastung pro Kern/Core:")
for i, perc in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
  print(f"Kern/Core {i}: {perc}%")

def adjust_size(size):
  factor = 1024
  for i in ["B", "KB", "MB", "GB", "TB", "PB"]:
    if size > factor:
      size = size / factor 
    else:
      return f"{size:.3f}{i}"

print('\n')
print("-"*40, "RAM Info", "-"*40)
print('\n')

virtual_mem = psutil.virtual_memory()
print(f"Gesamt: {adjust_size(virtual_mem.total)}")
print(f"Verwendet: {adjust_size(virtual_mem.used)}")
print(f"Verfügbar: {adjust_size(virtual_mem.available)}")
print(f"Prozentual: {virtual_mem.percent}%")

print('\n')
print("-"*42, "SWAP", "-"*42)
print('\n')

swap = psutil.swap_memory()
print(f"Gesamt: {adjust_size(swap.total)}")
print(f"Verwendet: {adjust_size(swap.used)}")
print(f"Frei: {adjust_size(swap.free)}")
print(f"Prozentual: {swap.percent}%")

print('\n')
print("-"*40, "DISK Info", "-"*39)
print('\n')

partitions = psutil.disk_partitions()
for p in partitions:
  print(f"Gerät: {p.device}")
  print(f"\tEingehängt: {p.mountpoint}")
  print(f"\tDatei System Typ: {p.fstype}")
  try:
    partition_usage = psutil.disk_usage(p.mountpoint)
  except PermissionError:
    continue
  print(f" Gesamt Grösse: {adjust_size(partition_usage.total)}")
  print(f" Verwendete: {adjust_size(partition_usage.used)}")
  print(f" Frei: {adjust_size(partition_usage.free)}")
  print(f" Prozentual: {partition_usage}%")


  disk_io = psutil.disk_io_counters()
  print(f"Seit Start gelesen: {adjust_size(disk_io.read_bytes)}")
  print(f"Seit Start geschrieben: {adjust_size(disk_io.write_bytes)}")


print('\n')
print("-"*40, "GRAKA Info", "-"*39)
print('\n')

gpus = GPUtil.getGPUs()
for gpu in gpus:
  print(f"ID: {gpu.id}, Name: {gpu.name}")
  print(f"\tLoad: {gpu.load*100}%")
  print(f"\tVerwendet: {gpu.memoryUsed}MB")
  print(f"\tFrei:: {gpu.memoryFree}MB")
  print(f"\tGesamt: {gpu.memoryTotal}MB")
  print(f"\tTemperatur: {gpu.temperature} °C")


print('\n')
print("-"*38, "Netzwerk Info", "-"*38)
print('\n')

if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
  for address in interface_addresses:
    print(f"Schnittstelle: {interface_name}")
    if str(address.family) == 'AddressFamily.AF_INET':
      print(f" IP Adresse: {address.address}")
      print(f" Netmask: {address.netmask}")
      print(f" Broadcast IP: {address.broadcast}")
    elif str(address.family) == 'AddressFamily.AF_PACKET':
      print(f" MAC Adresse: {address.address}")
      print(f" Netmask: {address.netmask}")
      print(f" Broadcast MAC: {address.broadcast}")

net_io = psutil.net_io_counters()
print(f"Gesamt Bytes gesendet: {adjust_size(net_io.bytes_sent)}")
print(f"Gesamt Bytes erhalten: {adjust_size(net_io.bytes_recv)}")

