#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder."""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    The archive is stored in the versions folder with a timestamped name.

    Returns:
        str: The path to the created archive if successful, otherwise None.
    """
    if not os.path.exists("web_static"):
        return None

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    versions_dir = "versions"
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)

    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = os.path.join(versions_dir, archive_name)

    try:
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    except Exception:
        return None
