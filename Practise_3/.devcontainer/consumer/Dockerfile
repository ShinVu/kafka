FROM python 

# Install dependency
# Copy the current directory contents into the container at /workspace/src
COPY requirements.txt /workspace/src/
# Set the working directory in the container
WORKDIR /workspace/src
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


CMD ["sleep", "infinity"]