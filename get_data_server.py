import psutil
import platform
import socket
from datetime import datetime

def get_ip_address():
    try:
        # Mendapatkan nama host
        hostname = socket.gethostname()
        # Mendapatkan IP berdasarkan nama host
        ip_address = socket.gethostbyname(hostname)
        
        # Pastikan IP bukan localhost
        if ip_address.startswith("127."):
            # Cari IP dari semua antarmuka jaringan
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Tes koneksi ke DNS Google
            ip_address = s.getsockname()[0]
            s.close()
        
        return ip_address
    except Exception as e:
        return f"Could not retrieve IP: {e}"

def get_detailed_server_stats():
    stats = {}

    # Sistem dasar
    stats['System'] = platform.system()
    stats['Node Name'] = platform.node()
    stats['Release'] = platform.release()
    stats['Version'] = platform.version()
    stats['Machine'] = platform.machine()
    stats['Processor'] = platform.processor()

    # IP Server
    stats['IP Address'] = get_ip_address()

    # Uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    stats['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")

    # CPU
    stats['CPU Count'] = psutil.cpu_count(logical=True)
    stats['CPU Usage'] = psutil.cpu_percent(interval=1)

    # Memori
    virtual_memory = psutil.virtual_memory()
    stats['Total Memory'] = virtual_memory.total
    stats['Available Memory'] = virtual_memory.available
    stats['Used Memory'] = virtual_memory.used
    stats['Memory Usage (%)'] = virtual_memory.percent

    # Disk
    disk_usage = psutil.disk_usage('/')
    stats['Total Disk'] = disk_usage.total
    stats['Used Disk'] = disk_usage.used
    stats['Free Disk'] = disk_usage.free
    stats['Disk Usage (%)'] = disk_usage.percent

    # Jaringan
    net_io = psutil.net_io_counters()
    stats['Bytes Sent'] = net_io.bytes_sent
    stats['Bytes Received'] = net_io.bytes_recv

    return stats

# Contoh penggunaan
server_stats = get_detailed_server_stats()
for key, value in server_stats.items():
    print(f"{key}: {value}")
