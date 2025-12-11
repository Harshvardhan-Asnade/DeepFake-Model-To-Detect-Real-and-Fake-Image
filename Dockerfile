# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
# Update pip first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Create necessary directories for uploads if they don't exist
# Matches the UPLOAD_FOLDER path in app.py: '../frontend/static/uploads'
# Since we will run from /code/backend, relative path ../frontend/static/uploads resolves to /code/frontend/static/uploads
RUN mkdir -p frontend/static/uploads

# Grant write permissions to the uploads directory (important for non-root users in some environments)
RUN chmod 777 frontend/static/uploads

# Change working directory to backend because app.py relies on relative paths like '../model'
WORKDIR /code/backend

# Make port 7860 available to the world outside this container (Standard for HF Spaces)
EXPOSE 7860

# Run app.py when the container launches
# Host 0.0.0.0 is crucial for Docker
CMD ["python", "app.py"]
