import os
import configparser

class GitRepository:
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, '.git')

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f'Not a git repository {path}')
        
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, 'config')

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception('Configuration file missing')
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f'Unsupported repositoryformatversion {vers}')
    
    def repo_path(self, *path):
        """Compute path under repo's gitdir"""
        return os.path.join(self.gitdir, *path)
    
    def repo_file(self, *path, mkdir=False):
        """Same as repo_path, but create dirname(*path) if absent"""
        if self.repo_dir(*path[:-1], mkdir=mkdir):
            return self.repo_path(*path)
        
    def repo_dir(self, *path, mkdir=False):
        """Same as repo_path, but mkdir *path if absent"""

        path = self.repo_path(*path)

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

