# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .


# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
