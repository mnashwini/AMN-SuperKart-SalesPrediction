FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all frontend files into the container
COPY . .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Streamlit application on port 8501 and make it accessible externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]

# NOTE: Disable XSRF protection for easier external access in order to make batch predictions
