# Use an official Python runtime as the base image
FROM python:3.11
LABEL authors="Antspihl"

# Set the working directory in the container
WORKDIR /kassa-back

# Copy only essential files into the container
COPY app.py /kassa-back
COPY bill_handler.py /kassa-back
COPY sheet_handler.py /kassa-back
COPY requirements.txt /kassa-back
COPY Dockerfile /kassa-back
COPY sheets_api.json /kassa-back

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
ENV PORT=5000
EXPOSE 5000

# Define the command to run your Flask app with Gunicorn and enable logging
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]