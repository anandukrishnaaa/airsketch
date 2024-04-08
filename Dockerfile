# Use the official Python 3.12.0 image as the base image
FROM python:3.12.0

# Set the working directory in the container
WORKDIR /airsketch_django_app

# Copy the current directory contents into the container at /airsketch_django_app
COPY . /airsketch_django_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
