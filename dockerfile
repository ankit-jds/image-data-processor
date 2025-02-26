# Use official Python image
FROM python:3.11

RUN python -m pip install --upgrade pip setuptools wheel


# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "image_processor.wsgi:application"]
