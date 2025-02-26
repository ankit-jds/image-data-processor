# Use official Python image
FROM python:3.11

RUN python -m pip install --upgrade pip setuptools wheel


# Set the working directory inside the container
WORKDIR /app

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port 8000 for Django
EXPOSE 8000


# Copy supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Ensure the supervisord binary is available
RUN which supervisord

# Run supervisord to start Django & Celery together
CMD ["supervisord", "-c", "/etc/supervisord.conf"]