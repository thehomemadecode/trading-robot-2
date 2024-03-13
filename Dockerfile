# Start with an official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy just the Python requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# If you're compiling a Cython extension, ensure Cython is listed in your requirements.txt
# Alternatively, you can install Cython here directly:
# RUN pip install Cython

# Copy the rest of your application's source code
COPY . .

# Compile any necessary C extensions for Python
# Ensure your setup.py is configured correctly for this task
RUN python setup.py build_ext --inplace

# Run your initialization script
# Adjust the script path if necessary
RUN python initdata/init_multi.py

# The default command to run when starting the container
# This can be an application, a script, or simply a command to keep the container running
# For example, to keep the container running without a specific task:
WORKDIR /app/initdata

CMD python init_multi.py && /bin/sh



