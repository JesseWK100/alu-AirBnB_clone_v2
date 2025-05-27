#!/usr/bin/python3
from fabric import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Stores archive in versions/ folder with timestamp in the filename.
    Returns the archive path if successful, else None.
    """
    # Create versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    # Generate timestamp for filename
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"
    
    try:
        print(f"Packing web_static to {archive_path}")
        # Run tar command locally to create the archive
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        return None
