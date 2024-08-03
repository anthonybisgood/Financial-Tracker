# Use a specific version of Python
FROM python:3.9-slim-buster

# Install system dependencies and cron
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron \
    git \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/anthonybisgood/Financial-Tracker.git /app

# Set the working directory
WORKDIR /app

# Copy requirements.txt before installing dependencies
COPY requirements.txt /app/

RUN chmod +x src/*

# Install Python dependencies with verbose logging
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add a cron job (assuming you want to run the Python script daily at 7 AM)
COPY crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply cron job
RUN crontab /etc/cron.d/my-cron-job

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD ["cron", "-f"]