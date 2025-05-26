#!/usr/bin/env bash
# 0-setup_web_static.sh
# Sets up the web server for web_static deployments

set -e

# 1. Install Nginx if it’s not already installed
if ! dpkg -l | grep -q nginx; then
  apt-get update -y
  apt-get install -y nginx
fi

# 2. Create the directory structure
for dir in /data /data/web_static/releases/test /data/web_static/shared; do
  mkdir -p "$dir"
done

# 3. Create a simple test HTML file
cat > /data/web_static/releases/test/index.html <<-EOF
<html>
  <head></head>
  <body>
    Holberton School
  </body>
</html>
EOF

# 4. (Re)create the symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# 5. Ensure ubuntu user:group exists before chown
if ! id ubuntu &>/dev/null; then
  echo "User 'ubuntu' not found — creating it now"
  useradd -m ubuntu
fi
if ! getent group ubuntu &>/dev/null; then
  echo "Group 'ubuntu' not found — creating it now"
  groupadd ubuntu
fi

chown -R ubuntu:ubuntu /data

# 6. Update Nginx config to serve /hbnb_static/
nginx_conf=/etc/nginx/sites-available/default
if ! grep -q "location /hbnb_static/" "$nginx_conf"; then
  sed -i '/server_name _;/a \\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }\n' "$nginx_conf"
fi

# 7. Restart Nginx
service nginx restart

exit 0
