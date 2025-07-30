ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    py3-pip \
    sqlite \
    curl

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    requests \
    aiohttp \
    asyncio \
    pyyaml

# Create app directory
WORKDIR /app

# Copy data for add-on
COPY run.sh /
COPY run.py /app/
COPY pv_forecast_comparison.py /app/
COPY pv_data_retriever.py /app/

# Make scripts executable
RUN chmod a+x /run.sh

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 8123

# Start the application
CMD [ "/run.sh" ] 