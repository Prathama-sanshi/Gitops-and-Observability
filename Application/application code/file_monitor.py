import os
import random
import time
import threading
import glob
import psutil
from prometheus_client import Gauge, start_http_server
from prometheus_client.core import REGISTRY

# Configuration from environment variables with defaults
MONITORED_DIR = os.getenv("MONITORED_DIR", "./monitored_files")
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "5"))
GENERATOR_INTERVAL = int(os.getenv("GENERATOR_INTERVAL", "3"))
DELETER_INTERVAL = int(os.getenv("DELETER_INTERVAL", "3"))
NAMESPACE = os.getenv("NAMESPACE", "default")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

# Ensure monitored directory exists
os.makedirs(MONITORED_DIR, exist_ok=True)

# Prometheus metrics
files_count = Gauge(
    'files_count',
    'Number of files in monitored directory by type',
    ['file_type', 'namespace', 'environment']
)

# System metrics
cpu_percent = Gauge(
    'cpu_percent',
    'CPU usage percentage',
    ['namespace', 'environment']
)

memory_percent = Gauge(
    'memory_percent',
    'Memory usage percentage',
    ['namespace', 'environment']
)

disk_percent = Gauge(
    'disk_percent',
    'Disk usage percentage',
    ['namespace', 'environment']
)


def count_files():
    """Count .log and .txt files in the monitored directory."""
    log_files = glob.glob(os.path.join(MONITORED_DIR, "*.log"))
    txt_files = glob.glob(os.path.join(MONITORED_DIR, "*.txt"))
    
    return len(log_files), len(txt_files)

def update_system_metrics():
    """Update system metrics (CPU, memory, disk)."""
    # CPU metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_percent.labels(namespace=NAMESPACE, environment=ENVIRONMENT).set(cpu_usage)
    
    # Memory metrics
    memory = psutil.virtual_memory()
    memory_percent.labels(namespace=NAMESPACE, environment=ENVIRONMENT).set(memory.percent)
    
    # Disk metrics - use current drive on Windows
    if os.name == 'nt':
        disk_path = os.path.splitdrive(os.getcwd())[0] + os.sep
    else:
        disk_path = '/'
    disk = psutil.disk_usage(disk_path)
    disk_percent.labels(namespace=NAMESPACE, environment=ENVIRONMENT).set(disk.percent)
    
    print(f"[System Metrics] CPU: {cpu_usage}%, Memory: {memory.percent}%, Disk: {disk.percent}%")

def update_metrics():
    """Update Prometheus metrics with current file counts."""
    log_count, txt_count = count_files()
    files_count.labels(file_type='log', namespace=NAMESPACE, environment=ENVIRONMENT).set(log_count)
    files_count.labels(file_type='txt', namespace=NAMESPACE, environment=ENVIRONMENT).set(txt_count)
    print(f"[File Metrics] log: {log_count}, txt: {txt_count}")

def file_generator():
    """Randomly create .log and .txt files."""
    while True:
        # Random number of files to create (1-3)
        num_files = random.randint(1, 3)
        
        for _ in range(num_files):
            file_type = random.choice(['log', 'txt'])
            timestamp = int(time.time())
            filename = f"file_{timestamp}_{random.randint(1000, 9999)}.{file_type}"
            filepath = os.path.join(MONITORED_DIR, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"Sample {file_type} file created at {timestamp}\n")
            
            print(f"[Generator] Created: {filename}")
        
        time.sleep(GENERATOR_INTERVAL)

def file_deleter():
    """Randomly delete files from the monitored directory."""
    while True:
        all_files = glob.glob(os.path.join(MONITORED_DIR, "*.*"))
        
        if all_files:
            # Random number of files to delete (1-2)
            num_to_delete = min(random.randint(1, 2), len(all_files))
            files_to_delete = random.sample(all_files, num_to_delete)
            
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"[Deleter] Deleted: {os.path.basename(filepath)}")
                except (PermissionError, OSError) as e:
                    print(f"[Deleter] Error deleting {os.path.basename(filepath)}: {e}")
        
        time.sleep(DELETER_INTERVAL)

def metrics_updater():
    """Periodically update metrics."""
    while True:
        update_metrics()
        update_system_metrics()
        time.sleep(UPDATE_INTERVAL)

def main():
    print("Starting File Monitor Application...")
    print(f"Monitoring directory: {os.path.abspath(MONITORED_DIR)}")
    print(f"Metrics endpoint: http://localhost:{METRICS_PORT}/metrics")
    
    # Start Prometheus HTTP server
    start_http_server(METRICS_PORT)
    
    # Start background threads
    generator_thread = threading.Thread(target=file_generator, daemon=True)
    deleter_thread = threading.Thread(target=file_deleter, daemon=True)
    metrics_thread = threading.Thread(target=metrics_updater, daemon=True)
    
    generator_thread.start()
    deleter_thread.start()
    metrics_thread.start()
    
    # Initial metrics update
    update_metrics()
    
    print("Application running. Press Ctrl+C to stop.")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
