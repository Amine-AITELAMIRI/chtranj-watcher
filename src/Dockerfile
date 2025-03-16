FROM python:3.8-slim

# Install dependencies and Chromium browser for Selenium
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Set working directory and copy files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables if needed (optional, can also set via Render dashboard)
ENV CHESS_URL="https://www.chess.com/login/"
ENV PROFILE_URL="https://www.chess.com/member/{}"
ENV BACKEND_URL="https://cg-s5v9.onrender.com"
ENV USERNAME="SMURFEEE"
ENV PASSWORD="Aminousa1"
ENV USERNAME_TO_WATCH="amphetamine4003"

# Start command to run continuously
CMD ["python", "src/headless.py"]