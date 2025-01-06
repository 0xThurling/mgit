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

argparser = argparse.ArgumentParser(description='Manage git repositories')
argsubparsers = argparser.add_subparsers(title='Commands', dest='command')
argsubparsers.required = True

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
