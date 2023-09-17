# Use a base image with Nix installed
FROM nixos/nix

# Clone the python-iavl repository
RUN nix-env -i git
RUN git clone https://github.com/crypto-com/python-iavl.git

# Enable the flakes experimental feature
RUN nix-env -iA nixpkgs.git
RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

# Set the working directory
WORKDIR /python-iavl

# Expose a port for any services (if necessary)
EXPOSE 80
RUN ["nix", "run", "github:crypto-com/python-iavl/#iavl-cli", "--", "--help"]
# Run the CLI tool as a Nix flake
ENTRYPOINT ["nix", "run", "github:crypto-com/python-iavl/#iavl-cli", "--"]

# Specify default arguments that can be overridden
CMD ["--help"]
