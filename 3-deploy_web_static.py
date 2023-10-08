#!/usr/bin/python3
"""
This script  creates and distributes an
archive to web servers.
"""


from datetime import datetime
from fabric.api import *
import os


env.user = 'ubuntu'
env.hosts = ['34.207.57.13', '54.174.203.20']


def do_pack():
    """
    Generates a .tgz archive.
    Returns:
        Archive path if successful
    """

    try:
        local("mkdir -p versions")
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"sudo tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        return f"Error: {e}"


def do_deploy(archive_path):
    """
    deployment script for my servers
    """

    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_noext = os.path.splitext(archive_filename)[0]

        # Upload archive to server
        put(archive_path, "/tmp/")

        # Uncompress the archive
        run(f"mkdir -p /data/web_static/releases/{archive_noext}/")
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_noext))

        # Delete the archive from the server
        run(f"rm /tmp/{archive_filename}")

        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(archive_noext, archive_noext))

        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_noext))

        # Delete and create a new symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_noext))
        print("New version deployed!")

        return True
    except Exception:
        return False


def deploy():
    """ Creates and distributes archives to web servers """

    archive_path_new = do_pack()
    if not os.path.exists(archive_path_new):
        return False

    response = do_deploy(archive_path_new)

    return response
