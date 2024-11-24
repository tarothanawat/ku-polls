# Use Python Alpine for a lightweight base image
FROM python:3-alpine

# Set working directory
WORKDIR /app/polls

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port for the application
EXPOSE 8000

# Use an entrypoint script to manage database setup and start the server
ENTRYPOINT ["sh", "/app/polls/entrypoint.sh"]
