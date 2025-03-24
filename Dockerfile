FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auto_sun_brightness.py .
COPY setup.py .
COPY README.md .

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "auto_sun_brightness.py"]

# Default command line arguments (can be overridden)
CMD ["--help"] 