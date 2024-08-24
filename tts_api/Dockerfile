# ./tts_api/Dockerfile

# Base image with CUDA
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04 as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # CUTLASS_PATH=/home/ubuntu/cutlass \
    DEBIAN_FRONTEND=noninteractive \
    CUDA_HOME=/usr/local/cuda \
    PATH=${CUDA_HOME}/bin:${PATH} \
    LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}


ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common curl git build-essential gcc g++ \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
    libsndfile1 ffmpeg libaio-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.9.19
RUN wget https://www.python.org/ftp/python/3.9.19/Python-3.9.19.tgz \
    && tar xzf Python-3.9.19.tgz \
    && cd Python-3.9.19 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.9.19 Python-3.9.19.tgz

# Install pip for Python 3.9.19
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py && rm get-pip.py

# Set Python 3.9.19 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1 \
    && update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements-new.txt .

# Use a persistent volume for pip cache
VOLUME /root/.cache/pip

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --use-feature=fast-deps -r requirements-new.txt

# Copy the entire tortoise directory
COPY tortoise ./tortoise

# Copy the download script
COPY download_models.py .

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run the download script
RUN python3 download_models.py

# Now copy the rest of the application
COPY . .

# Final stage
# FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # CUTLASS_PATH=/home/ubuntu/cutlass
    DEBIAN_FRONTEND=noninteractive \
    CUDA_HOME=/usr/local/cuda \
    PATH=${CUDA_HOME}/bin:${PATH} \
    LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 ffmpeg libaio-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python from builder
COPY --from=builder /usr/local/bin/python3.9 /usr/local/bin/python3.9
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=builder /usr/local/lib/libpython3.9.so* /usr/local/lib/

# Set Python 3.9.19 as the default python version
RUN ln -s /usr/local/bin/python3.9 /usr/local/bin/python \
    && ln -s /usr/local/bin/python3.9 /usr/local/bin/python3

RUN ls -l /usr/local/cuda/bin/nvcc || echo "nvcc not found"
RUN nvcc -V || echo "nvcc command not found"

WORKDIR /app

# Copy installed packages and application from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python3", "app.py"]