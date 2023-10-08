#!/usr/bin/python3
"""
This script distributes an archive
to my web servers.
"""


from datetime import datetime
from fabric.api import *
import os


print("First")
env.user = 'ubuntu'
env.hosts = ['34.207.57.13', '54.174.203.20']
print("Second")


def do_deploy(archive_path):
    """
    deployment script for my servers
    """
    print("Third")

    if not os.path.exists(archive_path):
        print("===> Archive path does not exist")
        return False

    try:
        print("Fourth")
        archive_filename = os.path.basename(archive_path)
        print(f"====> {archive_filename}")
        archive_noext = os.path.splitext(archive_filename)[0]
        print(f"====> {archive_noext}")

        # Upload archive to server
        put(archive_path, "/tmp/")
        print("Fifth")

        # Uncompress the archive
        run(f"mkdir -p /data/web_static/releases/{archive_noext}/")
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_noext))
        print("Sixth")

        # Delete the archive from the server
        run(f"rm /tmp/{archive_filename}")

        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(archive_noext, archive_noext))
        print("Seventh")

        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_noext))
        print("Eightth")

        # Delete and create a new symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_noext))
        print("New version deployed")

        return True
    except Exception:
        return False
