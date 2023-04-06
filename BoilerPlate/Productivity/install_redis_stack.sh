#!/bin/bash
set -euo pipefail

####
# file: install_redis_stack.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 4/5/2023
# revised: 4/5/2023
# reminder: chmod +x install_redis_stack.sh
# warning: This script is still a draft has not been tested yet
# This script sets redis, redis: json, search, graph, timeseries, bloom

#!/bin/bash
#!/bin/bash

# Update system and packages
sudo pacman -Syu --noconfirm

# Install Redis server and CLI
sudo pacman -S --noconfirm --needed redis

# Install build tools and required dependencies
sudo pacman -S --noconfirm --needed base-devel git

if [ ! -d /usr/bin/yay ]; then
  git clone https://aur.archlinux.org/yay.git ~/yay && sudo mv ~/yay /usr/bin/
fi
cd /usr/bin/yay/
makepkg -si --noconfirm
cd -



# Clone and build Redis modules
repos=(
  "https://github.com/RediSearch/RediSearch.git"
  "https://github.com/RedisJSON/RedisJSON.git"
  "https://github.com/RedisGraph/RedisGraph.git"
  "https://github.com/RedisTimeSeries/RedisTimeSeries.git"
  "https://github.com/RedisBloom/RedisBloom.git"
)

modules=("RediSearch" "RedisJSON" "RedisGraph" "RedisTimeSeries" "RedisBloom")

for i in "${!repos[@]}"; do
  repo="${repos[i]}"
  module="${modules[i]}"
  
#   if [ ! -d "${module}" ]; then
  git clone --recursive "$repo"
#   fi


  cd "${module}"
#   sed -i 's#os.path.isfile("/usr/bin/yay")#os.path.isdir("/usr/bin/yay")#' /home/adminjay/Pegboard/BoilerPlate/Productivity/RediSearch/deps/readies/paella/setup.py
  echo "Press any key to continue..."
  read -n 1 -s -r -p ""
  ./sbin/setup

  make
  sudo cp "${module}.so" "/usr/lib/"
  cd ..
done


# Create a Redis configuration file with modules
sudo bash -c "cat > /etc/redis/redis.conf << EOL
loadmodule /usr/lib/RedisJSON.so
loadmodule /usr/lib/RediSearch.so
loadmodule /usr/lib/RedisGraph.so
loadmodule /usr/lib/RedisTimeSeries.so
loadmodule /usr/lib/RedisBloom.so
bind 127.0.0.1
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile /var/log/redis/redis.log
databases 16
always-show-logo yes
EOL"

# Enable and start Redis server
sudo systemctl enable redis
sudo systemctl start redis

# Print Redis server status
sudo systemctl status redis
