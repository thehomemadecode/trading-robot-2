# Start with the Node.js version 14 base image
FROM node:14-bullseye

# Set the working directory in the container
WORKDIR /app

# Install Python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential 

# Install Cython, if it's a dependency for compiling your C extension
RUN pip3 install Cython

# Copy package.json and package-lock.json (if available) for Node.js dependencies
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the setup script, C source file, and other necessary Python files
COPY setup.py trobot2module.c ./
COPY initdata/ initdata/

# Compile the C extension module. This step generates the .pyd or .so file.
RUN python3 setup.py build_ext --inplace

# Now, run the initialization script from the initdata directory
RUN python3 initdata/init_multi.py

# Copy the rest of your application's code
COPY . .

# Expose the port your app runs on, adjust as needed (e.g., for a Node.js app)
EXPOSE 3000

# Command to run your app, adjust according to how you start your Node.js application
CMD ["node", "src/server.js"]
