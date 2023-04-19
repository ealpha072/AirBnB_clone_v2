#!/usr/bin/python3
"""creates and distributes an archive to web servers"""
from fabric.api import *
do_deploy = __import__('2-do_deploy_web_static').do_deploy
do_pack = __import__('1-pack_web_static').do_pack

env.hosts = ['100.24.235.35', '100.26.158.195']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'
archive = 'versions/web_static_20230405212617.tgz'


def deploy():
    """Implementation"""
    try:
        archive_path = do_pack()
        if archive_path == False:
            return False
        else:
            return do_deploy(archive_path)
    except Exception:
        return False


deploy()
