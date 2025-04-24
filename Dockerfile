# Use the official Python image as the base image
FROM python:3.9

# Set up a non-root user for security
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container and install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application files into the container
COPY --chown=user . /app

# Expose the port that Hugging Face Spaces requires
EXPOSE 7860

# Set the default command to run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
