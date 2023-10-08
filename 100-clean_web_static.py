#!/usr/bin/python3
"""
This script that deletes out-of-date archives.
"""


from datetime import datetime
from fabric.api import *
import os


env.user = 'ubuntu'
env.hosts = ['34.207.57.13', '54.174.203.20']


def do_clean(number=0):
    """
    Deletes out-of-date archives from versions & releases folders.
    """

    try:
        number = int(number)
    except ValueError:
        return

    if number < 0:
        return

    number = 1 if number == 0 else number + 1

    # Clean up local versions folder
    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs -I {{}} rm {{}}'.format(number))

    # Clean up remote versions folder
    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}'.format(number))
