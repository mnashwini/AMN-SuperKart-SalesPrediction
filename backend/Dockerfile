FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install dependencies from the requirements file without using cache
# to reduce the image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Flask application using Gunicorn
# -w 4: Uses 4 worker processes
# -b 0.0.0.0:7860: Binds the server to port 7860 on all network interfaces
# app:superkart_sales_predictor_api:
# Runs the Flask application defined in app.py

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_sales_predictor_api"]
