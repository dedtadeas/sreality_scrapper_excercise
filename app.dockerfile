# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install app dependencies and Gunicorn
COPY /app/requirements.txt .
RUN pip install -r requirements.txt gunicorn

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask app files to the container
COPY app .

# Expose port 8080 for the Flask app
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "sreality_presenter:app", "-b", "0.0.0.0:8080"]