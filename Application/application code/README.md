# File Monitor - Prometheus Custom Metrics Demo

A simple application that demonstrates Prometheus custom metrics by monitoring file counts in a directory. The application randomly creates and deletes `.log` and `.txt` files, exposing the counts as Prometheus metrics with labels.

## Features

- **File Monitoring**: Tracks `.log` and `.txt` files in a monitored directory
- **Random File Generation**: Background thread creates files at random intervals
- **Random File Deletion**: Background thread deletes files at random intervals
- **Prometheus Metrics**: Exposes `files_count` gauge metric with `file_type` label
- **Real-time Updates**: Metrics updated every 5 seconds

## Architecture

### Components

1. **File Generator**: Creates 1-3 random files every 3 seconds
2. **File Deleter**: Deletes 1-2 random files every 4 seconds
3. **Metrics Updater**: Counts files and updates Prometheus metrics every 5 seconds
4. **HTTP Server**: Exposes metrics on port 8000

### Prometheus Metric

```
files_count{file_type="log"} - Number of .log files
files_count{file_type="txt"} - Number of .txt files
```

## Setup

### Prerequisites

- Python 3.8+
- uv (Python package manager)

### Installation

1. **Create virtual environment using uv**:
   ```bash
   uv venv
   ```

2. **Activate the virtual environment**:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Run the Application

```bash
python file_monitor.py
```

The application will:
- Create a `monitored_files` directory
- Start the Prometheus metrics server on `http://localhost:8000/metrics`
- Begin generating and deleting files in the background
- Update metrics every 5 seconds

### Access Metrics

Open your browser or use curl:
```bash
curl http://localhost:8000/metrics
```

You should see output like:
```
# HELP files_count Number of files in monitored directory by type
# TYPE files_count gauge
files_count{file_type="log"} 5.0
files_count{file_type="txt"} 3.0
```

## Prometheus Configuration

Add this to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'file_monitor'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 5s
```

Restart Prometheus to apply the configuration.

## Grafana Dashboard

### Recommended Queries

1. **Show all file types**:
   ```
   files_count
   ```

2. **Filter by specific type**:
   ```
   files_count{file_type="log"}
   ```

3. **Total files**:
   ```
   sum(files_count)
   ```

4. **Stacked area chart**:
   ```
   files_count
   ```
   Format as: Stack

### Panel Suggestions

- **Time Series**: Show file count over time
- **Stat**: Display current total file count
- **Gauge**: Visualize current counts by file type

## Configuration

You can modify these constants in `file_monitor.py`:

```python
MONITORED_DIR = Path("./monitored_files")  # Directory to monitor
METRICS_PORT = 8000                         # Metrics server port
UPDATE_INTERVAL = 5                         # Metrics update interval (seconds)
GENERATOR_INTERVAL = 3                      # File generation interval (seconds)
DELETER_INTERVAL = 4                        # File deletion interval (seconds)
```

## Stopping the Application

Press `Ctrl+C` to stop the application gracefully.

## Cleanup

To remove the monitored files and directory:
```bash
rm -rf monitored_files
```

## Troubleshooting

- **Port already in use**: Change `METRICS_PORT` in `file_monitor.py`
- **Permission errors**: Ensure write permissions for the monitored directory
- **Metrics not updating**: Check that the application is running and no errors are displayed
