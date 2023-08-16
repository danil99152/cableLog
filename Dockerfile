# Use latest Python 3.11 image as the base image
FROM python:3.11

# Copy the application code to the working directory (root)
COPY core core

# Install dependencies from requirements.txt
RUN pip install -r core/requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Set environment variable for Streamlit port
ENV STREAMLIT_SERVER_PORT 8501

# Run the Streamlit app
CMD streamlit run core/main.py

# Build image command
# docker build -t cablelog .

# Run container command
# docker run -e LOGIN=<login> -e PASSWORD=<password> -p 8501:8501 --name cabelog cablelog
# Write your <login> and <password>