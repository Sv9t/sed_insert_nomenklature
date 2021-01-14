#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import base64
import hashlib
import requests


class VariableUrlGitLab:
    HOST = 'Z2l0bGFiLmxvY2FsL2dyb3VwL3B5dGhvbl9wcm9kdWN0aW9uL2luc2VydF9ub21la2xhdHVyZS9yYXcvbWFzdGVyL21vZHVsZQ=='
    VERSION_HOST = 'Z2l0bGFiLmxvY2FsL2dyb3VwL3B5dGhvbl9wcm9kdWN0aW9uL2luc2VydF9ub21la2xhdHVyZS9yYXcvbWFzdGVyL21vZHVsZS9tb2RfY29udHJvbC5weQ=='
    VERSION_LOCAL = '20.12.03'


def read_hash(*args):
    """
    Read hash md5 module file
    """
    hasher = hashlib.md5()
    with open(args[0], 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()


def replace_file(*args):
    """
    Replace
    """
    path = r'main\httpimport.py'
    path_src = os.path.join(args[0], path)
    shutil.copyfile(path_src, args[1])


def read_remote_version():
    """
    Read remote file from gitlab and return version 
    """
    r = requests.get(base64.b64decode(
        VariableUrlGitLab.VERSION_HOST).decode(), stream=True)
    for string in r.raw:
        if b'VERSION' in string:
            sting_version = str(string).split("'")[1]
            break
    return sting_version


def control_version():
    """
    ### TODO ###
    Verify control version scripts on gitlab
    """
    t = True
    if read_remote_version() != VariableUrlGitLab.VERSION_LOCAL:
        t = False
    return t


def control_hhtpimport(*args):
    """
    Verify local module and replace
    """
    path_to_file = r'env_gitlab\Lib\site-packages\httpimport.py'
    path_env = os.path.join(args[0], path_to_file)
    hash_orig = '48b73a44b30afead1c29079e7fa7a7ec'
    hash_new = read_hash(path_env)
    
    if hash_orig != hash_new:
        replace_file(args[0], path_to_file)
