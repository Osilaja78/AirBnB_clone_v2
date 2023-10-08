#!/usr/bin/python3
"""
This  Fabric script that generates a .tgz archive
from the contents of the web_static folder.
"""


from fabric.api import *
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive.
    Returns:
        Archive path if successful
    """

    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvfz {archive_path} web_static")
        return archive_path
    except Exception as e:
        return f"Error: {e}"
