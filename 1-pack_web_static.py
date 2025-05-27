#!/usr/bin/python3
"""
Fabric script (1-pack_web_static.py) that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo.
Usage:
    $ fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    - Archives all files within web_static.
    - Creates versions/ folder if it doesn't exist.
    - Names the archive web_static_<YYYYMMDDHHMMSS>.tgz.

    Returns:
        str: Path to the created archive, or None if failure.
    """
    # Ensure versions directory exists
    versions_dir = "versions"
    if not os.path.isdir(versions_dir):
        os.makedirs(versions_dir)

    # Generate archive filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join(versions_dir, archive_name)

    # Create the archive
    try:
        local(f"tar -cvzf {archive_path} web_static/")
        print(f"web_static packed: {archive_path} -> {os.path.getsize(archive_path)}Bytes")
        return archive_path
    except Exception:
        return None
