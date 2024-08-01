# Dockerfile
FROM python:3.8-slim-buster

# Install cron and git
RUN apt-get update && apt-get -y install cron git

# Clone the repository
RUN git clone https://github.com/anthonybisgood/Financial-Tracker.git /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt
