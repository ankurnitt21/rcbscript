# Use an official lightweight Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install

# Run the script
CMD ["python", "script1.py"]
