#!/usr/bin/python3
"""Distributes an archive to web servers"""
import os
from fabric.api import *
from pathlib import Path


env.hosts = ['100.24.235.35', '100.26.158.195']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Implementation"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        filename = os.path.basename(archive_path)
        filename_no_ext = os.path.splitext(filename)[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(filename_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, filename_no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'\
            .format(filename_no_ext, filename_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'\
            .format(filename_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename_no_ext))
        run('sudo service nginx restart')
        return True
    except Exception:
        return False
