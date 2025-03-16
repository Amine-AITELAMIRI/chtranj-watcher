# Use Python base image
FROM python:3.8-slim

# Install system dependencies for ChromeDriver and Chromium
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium-browser \
    wget \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port for the HTTP server (default Render port is 8080)
EXPOSE 8080

# Set environment variables for the script (optional, can also be set via Render dashboard)
ENV CHESS_URL="https://www.chess.com/login/"
ENV PROFILE_URL="https://www.chess.com/member/{}"
ENV BACKEND_URL="https://cg-s5v9.onrender.com"
ENV USERNAME="SMURFEEE"
ENV PASSWORD="Aminousa1"
ENV USERNAME_TO_WATCH="amphetamine4003"

# Command to run the Python script
CMD ["python", "src/headless.py"]
