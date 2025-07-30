FROM python:3.12-slim-bookworm

WORKDIR /app

# First, install system dependencies including Supervisor
# Combining RUN commands reduces layer size
RUN apt-get update && apt-get install -y \
    awscli \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the supervisor configuration file to the correct location in the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the Streamlit port, which will be our public-facing service
EXPOSE 8501

# The main command to run when the container starts.
# This starts Supervisor, which in turn starts FastAPI and Streamlit.
CMD ["/usr/bin/supervisord"]