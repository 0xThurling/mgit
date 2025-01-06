import argparse
import collections
import configparser
from datetime import datetime
import grp, pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib
from gitrepositoty import GitRepository

argparser = argparse.ArgumentParser(description='Manage git repositories')
argsubparsers = argparser.add_subparsers(title='Commands', dest='command')
argsubparsers.required = True

def repo_path(repo, *path):
      """Compute path under repo's gitdir"""
      return os.path.join(repo.gitdir, *path)
  
def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent"""

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)
    
def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent"""

    path = repo_path(repo, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f'Not a directory {path}')
        
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None
    
def repo_create(path):
    """Create a new repository in path"""

    repo = GitRepository(path=path, force=True)

    # First, we make sure the path either doesn't exist or is an
    # empty dir.

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory")
        if not os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case 'add': cmd_add(args)
        case 'cat-file': cmd_cat_file(args)
        case 'checkout': cmd_checkout(args)
        case 'commit': cmd_commit(args)
        case 'hash-object': cmd_hash_object(args)
        case 'init': cmd_init(args)
        case 'log': cmd_log(args)
        case 'ls-tree': cmd_ls_tree(args)
        case 'merge': cmd_merge(args)
        case 'rebase': cmd_rebase(args)
        case 'rev-parse': cmd_rev_parse(args)
        case 'rm': cmd_rm(args)
        case 'show-ref': cmd_show_ref(args)
        case 'tag': cmd_tag(args)
        case _ : print("Bad Command")
