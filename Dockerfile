# Use the official Playwright image with all dependencies pre-installed
FROM mcr.microsoft.com/playwright/python:v1.42.0

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "script1.py"]
