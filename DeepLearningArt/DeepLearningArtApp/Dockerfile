# Use an official Python runtime as a parent image
FROM python:3.6

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80

# CMD specifcies the command to execute to start the server running.
CMD ["/app/DeepLearningArtApp/entrypoint.sh"]