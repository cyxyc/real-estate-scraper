# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirementsFORDOCKER.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run db.py when the container launches
CMD ["uvicorn", "db:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

