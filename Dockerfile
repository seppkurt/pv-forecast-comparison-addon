FROM python:3.9-alpine

# Install required packages
RUN apk add --no-cache \
    sqlite \
    curl \
    && pip3 install --no-cache-dir \
    requests \
    aiohttp \
    asyncio

# Create app directory
WORKDIR /app

# Copy application files
COPY run.py /app/
COPY pv_forecast_comparison.py /app/
COPY pv_data_retriever.py /app/
COPY config.yaml /app/

# Make scripts executable
RUN chmod +x /app/run.py

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 8123

# Start the application
CMD ["python3", "/app/run.py"] 