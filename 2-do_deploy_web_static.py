#!/usr/bin/python3
"""
Distributes an archive to web servers using Fabric.

Usage:
    fab do_deploy:archive_path=versions/web_static_YYYYmmddHHMMSS.tgz

Environment:
    env.hosts: list of web server IPs
    env.user:   remote user (ubuntu)
    env.key_filename: path to your SSH private key (optional)
"""

import os
from fabric.api import env, put, run

# ====== CONFIGURE YOUR SERVERS HERE ======
env.hosts = ['34.205.18.224', '44.204.39.103']
env.user = 'ubuntu'
# env.key_filename = '/home/ubuntu/.ssh/id_rsa'
# =========================================

def do_deploy(archive_path):
    """
    Upload and deploy a .tgz archive to web servers.
    Returns True on success, False on failure.
    """
    if not os.path.isfile(archive_path):
        return False

    filename = os.path.basename(archive_path)
    name = filename.rsplit('.', 1)[0]
    release_dir = f"/data/web_static/releases/{name}/"

    try:
        # 1. Upload archive to /tmp/
        put(archive_path, f"/tmp/{filename}")
        # 2. Create release directory
        run(f"mkdir -p {release_dir}")
        # 3. Uncompress into the new release dir
        run(f"tar -xzf /tmp/{filename} -C {release_dir}")
        # 4. Remove the uploaded archive
        run(f"rm /tmp/{filename}")
        # 5. Move content out of web_static folder
        run(f"mv {release_dir}web_static/* {release_dir}")
        # 6. Delete now-empty web_static folder
        run(f"rm -rf {release_dir}web_static")
        # 7. Remove current symlink
        run("rm -rf /data/web_static/current")
        # 8. Create new symlink
        run(f"ln -s {release_dir} /data/web_static/current")
        return True
    except Exception:
        return False
