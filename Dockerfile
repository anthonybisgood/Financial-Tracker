# Use a specific version of Python
FROM python:3.9-slim-buster

#Set Timezone
ENV TZ="US/Mountain"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies and cron
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    cron \
    git \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js (version 14.x, you can change the version as needed)
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/anthonybisgood/Financial-Tracker.git /app

# Set the working directory
WORKDIR /app

# Copy requirements.txt before installing dependencies
COPY requirements.txt /app/
COPY .env /app/

RUN chmod +x src/*

# Install Python dependencies with verbose logging
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
WORKDIR /app/src
RUN npm install ynab
RUN npm install dotenv
RUN npm install sqlite3

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