# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make scripts executable
RUN chmod +x setup_ubuntu.sh start_live.sh

# Create logs directory
RUN mkdir -p logs

# Expose port (if needed for web interface in future)
EXPOSE 8000

# Default command
CMD ["python", "main_pro.py"]