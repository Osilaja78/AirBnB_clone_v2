#!/usr/bin/env bash
# This script sets up web servers for deployment.

# Udate and install nginx if nt installed.
if ! dpkg -l | grep -q nginx; then
	apt-get update
	apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' > /data/web_static/releases/test/index.html

# symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
sed -i '/listen 80 default_server;/a \\n\tlocation /hbnb_static {\n\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
service nginx restart
