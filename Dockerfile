FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Script to wait for dependencies and start app
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"] 