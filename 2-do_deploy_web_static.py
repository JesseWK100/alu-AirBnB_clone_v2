#!/usr/bin/python3
"""
Distributes an archive to web servers using Fabric.

Functions:
    do_deploy(archive_path): Uploads and deploys the given .tgz archive
        to the web servers defined in env.hosts. Returns True on success;
        False otherwise.
"""
import os
from fabric.api import env, put, run

# Replace with your actual server IPs
env.hosts = ['34.205.18.224', '44.204.39.103']


def do_deploy(archive_path):
    """
    Distribute an archive to the web servers.

    Arguments:
        archive_path (str): Path to the .tgz archive to deploy.

    Returns:
        bool: True if all operations succeed, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    # Extract filename and base name
    archive_file = os.path.basename(archive_path)
    release_name = os.path.splitext(archive_file)[0]
    release_dir = f"/data/web_static/releases/{release_name}/"

    try:
        # Upload the archive to /tmp/
        put(archive_path, f"/tmp/{archive_file}")

        # Create the release directory
        run(f"mkdir -p {release_dir}")

        # Uncompress the archive into the release directory
        run(f"tar -xzf /tmp/{archive_file} -C {release_dir}")

        # Remove the uploaded archive from /tmp/
        run(f"rm /tmp/{archive_file}")

        # Move content out of the web_static folder
        run(f"mv {release_dir}web_static/* {release_dir}")

        # Remove the now-empty web_static directory
        run(f"rm -rf {release_dir}web_static")

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run(f"ln -s {release_dir} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception:
        return False
