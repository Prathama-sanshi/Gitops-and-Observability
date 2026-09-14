FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

#Install requiremetns 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the metrics port
EXPOSE 8000

# Run the application
CMD ["python", "file_monitor.py"]