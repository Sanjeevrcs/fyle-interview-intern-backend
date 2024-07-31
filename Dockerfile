# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that the application runs on
EXPOSE 7755

# Run gunicorn to serve the Flask application
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
