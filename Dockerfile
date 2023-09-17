# Use a base image with Nix installed
FROM nixos/nix

# Clone the python-iavl repository
RUN nix-env -i git

# Enable the flakes experimental feature
RUN nix-env -iA nixpkgs.git
RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

# Set the working directory
WORKDIR /python-iavl


RUN ["nix", "run", "github:tuky191/python-iavl/#iavl-cli-leveldb", "--", "--help"]
# Run the CLI tool as a Nix flake
ENTRYPOINT ["nix", "run", "github:tuky191/python-iavl/#iavl-cli-leveldb", "--"]

# Specify default arguments that can be overridden
CMD ["--help"]
