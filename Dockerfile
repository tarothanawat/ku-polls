
FROM python:3-alpine

# Install required system libraries for psycopg2 (PostgreSQL)
RUN apk add --no-cache build-base postgresql-dev musl-dev

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port for Django
EXPOSE 8000

# Run the app using the entrypoint script
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
