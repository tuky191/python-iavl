FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

# Install Poetry
RUN apt update -y
RUN apt install libleveldb-dev python3.9 python3-pip git python3.9-dev vim pkg-config -y
RUN apt install rocksdb-tools librocksdb5.17 librocksdb-dev libsnappy-dev liblz4-dev libbz2-dev -y
RUN python3.9 -m pip install poetry plyvel setuptools wheel

WORKDIR /python-iavl
# # Clone the GitHub repository
COPY . .

# # Set the working directory to the cloned repository

RUN export CFLAGS=-stdlib=libc++
# # Install the project dependencies using Poetry
RUN poetry install

# Copy the entrypoint script into the container
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]