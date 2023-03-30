#!/bin/bash
#chmod +x docker-redis-setup.sh
#drafted by: Evan Upham; evan.upham@outlook.com; https://www.uphamprojects.com
#drafted:3/25/2023
#revised:3/26/2023
# file: docker-redis-setup.sh
set -e
FLAGFILE="/tmp/docker-setup-reboot"

# List of dependencies
dependencies=("docker" "cronie")

# Install missing dependencies
for dep in "${dependencies[@]}"; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "Installing $dep..."
    sudo pacman -S "$dep"
  fi
done

# Check if Docker is already installed and configured to run without sudo
if ! docker info >/dev/null 2>&1; then

  if [ ! -f $FLAGFILE ]; then
    sudo pacman -Syu
    sudo pacman -S docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $(whoami)
    sudo systemctl start cronie

    # Create a flag file
    touch $FLAGFILE

    # Add a cron job to run this script on reboot if the flag file exists
    (crontab -l ; echo "@reboot [ -f $FLAGFILE ] && $(pwd)/docker-redis-setup.sh") | crontab -

    # Reboot the system
    sudo reboot
  else
    # Remove the flag file
    rm $FLAGFILE

    # Remove the cron job
    (crontab -l | grep -v "@reboot [ -f $FLAGFILE ] && /docker-redis-setup.sh") | crontab -



    # Check if the RedisGraph container exists and create it if it doesn't
    if ! docker ps -a | grep -q 'redis-stack-server'; then
      docker run -d -p 6379:6379 --name redis-server --rm redis/redis-stack-server
    fi

  fi
else
  echo "Docker is already installed and configured to run without sudo."
fi

# Wait for containers to be up and running
sleep 10

# Open a new terminal and print a success message
echo 'Docker, Redis, and RedisGraph have been successfully set up!'
echo 'Docker version:'; docker --version
echo 'Running containers:'; docker ps
echo 'Checking Redis connection:'; docker exec -it redis redis-cli ping
echo 'Checking RedisGraph connection:'
docker exec -it redisgraph redis-cli -p 6379 GRAPH.QUERY MyGraph "CREATE (:Node {name:'test'})"
docker exec -it redisgraph redis-cli -p 6379 GRAPH.QUERY MyGraph "MATCH (n) RETURN n"
read -p 'Press [Enter] to close this terminal...'
exit
