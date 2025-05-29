#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

from fabric.api import env, put, run
import os

# Configure Fabric environment
env.hosts = ['34.205.18.224', '44.204.39.103']  # Your web servers
env.user = 'ubuntu'  # SSH username
# env.key_filename = '~/.ssh/your_key.pem'  # Uncomment and set if using a specific SSH key

def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations succeed, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract archive name and base name (without .tgz)
        archive_name = os.path.basename(archive_path)
        base_name = archive_name[:-4]  # Remove .tgz extension
        release_dir = "/data/web_static/releases/{}".format(base_name)
        tmp_path = "/tmp/{}".format(archive_name)

        # Upload the archive to /tmp/ on the server
        put(archive_path, tmp_path)

        # Create the release directory
        run("mkdir -p {}".format(release_dir))

        # Uncompress the archive to the release directory
        run("tar -xzf {} -C {}".format(tmp_path, release_dir))

        # Delete the archive from /tmp/
        run("rm {}".format(tmp_path))

        # Move contents from web_static/ to release_dir (strip web_static folder)
        run("mv {}web_static/* {}".format(release_dir, release_dir))

        # Remove the now-empty web_static directory
        run("rm -rf {}web_static".format(release_dir))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    except Exception:
        return False
