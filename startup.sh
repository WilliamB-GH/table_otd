#!/usr/bin/env bash


sudo yum update -y

sudo yum install -y git

sudo yum install -y docker

sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker

# Docker buildx update steps taken from 
# https://github.com/amazonlinux/amazon-linux-2023/issues/1032#issuecomment-3874686692

# 1. Create the plugin directory if it doesn't exist
mkdir -p ~/.docker/cli-plugins

#2.Download the latest buildx binary from GitHub

ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
BUILDX_URL=$(curl -s https://api.github.com/repos/docker/buildx/releases/latest | grep "browser_download_url.*linux-$ARCH" | cut -d '"' -f 4)

curl -L $BUILDX_URL -o ~/.docker/cli-plugins/docker-buildx

# 3. Make it executable
chmod +x ~/.docker/cli-plugins/docker-buildx

# 4. Verify the version
docker buildx version


# Install docker compose as per: 
# https://www.reddit.com/r/docker/comments/1qm0rf6/comment/o1iwspe/

COMPOSE_VERSION="${COMPOSE_VERSION:-2.39.4}"
DOCKER_CONFIG="${DOCKER_CONFIG:-$HOME/.docker}"
PLUGIN_DIR="${PLUGIN_DIR:-$DOCKER_CONFIG/cli-plugins}"
SUDO="${SUDO:-}"
# system-wide: PLUGIN_DIR=/usr/local/lib/docker/cli-plugins; SUDO=sudo
# distro path (pkg-managed): PLUGIN_DIR=/usr/libexec/docker/cli-plugins; SUDO=sudo
$SUDO mkdir -p "$PLUGIN_DIR"
$SUDO curl -SL "https://github.com/docker/compose/releases/download/v${COMPOSE_VERSION}/docker-compose-linux-x86_64" -o "$PLUGIN_DIR/docker-compose"
$SUDO chmod +x "$PLUGIN_DIR/docker-compose"

# With all that faff out of the way...

git clone https://github.com/WilliamB-GH/table_otd.git
cd table_otd
docker compose up -d