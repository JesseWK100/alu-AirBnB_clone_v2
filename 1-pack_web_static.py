#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder."""

from fabric.api import local, settings
import os
from datetime import datetime

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    The archive is stored in the versions folder with a timestamped name.

    Returns:
        str: The path to the created archive if successful, otherwise None.
    """
    try:
        # Generate timestamp in the format YYYYMMDDHHMMSS
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        versions_dir = "versions"

        # Create versions directory if it doesn't exist
        if not os.path.exists(versions_dir):
            os.makedirs(versions_dir)

        # Define the archive path
        archive_path = os.path.join(versions_dir, f"web_static_{timestamp}.tgz")

        # Inform user about the packing process
        print(f"Packing web_static to {archive_path}")

        # Execute tar command with warn_only to handle failures gracefully
        with settings(warn_only=True):
            result = local(f"tar -cvzf {archive_path} web_static")

        # Check if the command was successful
        if result.succeeded:
            size = os.path.getsize(archive_path)
            print(f"web_static packed: {archive_path} -> {size}Bytes")
            return archive_path
        else:
            return None
    except Exception:
        return None
