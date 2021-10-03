#! /usr/bin/python3
import sys
import argparse
import os
import re


# import file
# for dir in file:
#     targetDirs.append(dir)

m3u_pattern =  re.compile('(?P<hidden_prefix>\.|)(?P<playlist_name>.*)\.m3u')

class Playlist:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.tracks = []
    def add_track(self, track):
        self.tracks.append(track)
    def import_m3u(self, file):
        if args.verbose :
            print('import file')
    def compare(self, another):
        if args.verbose :
            print('compare')
    def is_branch(self):
        return os.path.basename(self.path).removesuffix('.m3u') != self.name
#    def read_content(self):

#    def write_content(self):

class PlaylistTree:
    def __init__(self, name):
        self.name = name
        self.root_playlist = None
        self.branch_playlists = []
        self.tracks = []
#    def read_contents(self):
    def show(self):
        print(self.name)
        if self.root_playlist is None:
            print('  root: None')
        else:
            print('  root: ' + self.root_playlist.path)
        
        print('  branches:')
        for branch in self.branch_playlists:
            print ('    ' + branch.path)
        print('')
    
class PlaylistTrees:
    def __init__(self, args):
        self.root = args.directory
        self.prefix = args.tree_prefix
        self.suffix = args.tree_suffix
        self.tree_dict = None
        self.reflesh()

    def reflesh(self):
        if not os.path.isdir(self.root):
            print('Error: ' + self.root + ' is not directory')

        self.tree_dict = {}
        for root, dirs, files in os.walk(self.root):
            for name in files:
                self.parse_tree_dict(os.path.join(root, name))
    
    def parse_tree_dict(self, path):
        dir = os.path.dirname(path)
        file = os.path.basename(path)
        if (not(file.startswith(self.prefix) and file.endswith(self.suffix))) and (not (file.endswith('.m3u') and os.path.samefile(dir, self.root))):
            return
        
        playlist_name = file.removeprefix(self.prefix).removesuffix(self.suffix).removesuffix('.m3u')
        playlist = Playlist(path, file.removeprefix(self.prefix).removesuffix(self.suffix).removesuffix('.m3u'))

        if not ( playlist.name in self.tree_dict):
            tree = PlaylistTree(playlist.name)      
            self.tree_dict[playlist.name] = tree
        else :
            tree = self.tree_dict.get(playlist.name)

        if playlist.is_branch():
            tree.branch_playlists.append(playlist)
        else:
            tree.root_playlist = playlist
    
            
    def show(self):
        for tree in self.tree_dict.values():
            tree.show()


playlist_dict = {}

def show_m3u(targetDirPath):
    result = []
    if not os.path.isdir(targetDirPath):
        print('Error: ' +targetDirPath + ' is not directory')

    for root, dirs, files in os.walk(targetDirPath):
        for name in files:
            # m3u_match =  m3u_pattern.fullmatch(name)
            # if m3u_match:
            if name.endswith('.m3u'):
                result.append(os.path.abspath(os.path.join(root, name)))
                #if args.verbose :
                #    print(name)
    return result
def show_m3u_tree(rootDir):
    result = {}
    playlists = show_m3u(rootDir)
        


def m3ut_compile(args):
    print('m3u-tools compile')
    load_m3u(args.directory)

def m3ut_show(args):
    print('m3u-tools show')
    print(PlaylistTrees(args).show())

def m3ut_check(args):
    print('m3u-tools check')
    print(load_m3u(args.directory))

def m3ut_split(args):
    print('m3u-tools split')

def m3ut_fix(args):
    print('m3u-tools fix')

parser = argparse.ArgumentParser(description='Merging same name m3u files')
subparsers = parser.add_subparsers(help='sub-command help')

parser_compile = subparsers.add_parser('compile', help='compile help')
parser_compile.set_defaults(func=m3ut_compile)

parser_check = subparsers.add_parser('check', help='check help')
parser_check.set_defaults(func=m3ut_check)

parser_split = subparsers.add_parser('split', help='split help')
parser_split.set_defaults(func=m3ut_split)

parser_fix = subparsers.add_parser('fix', help='fix help')
parser_fix.set_defaults(func=m3ut_fix)

parser_show = subparsers.add_parser('show', help='show help')
parser_show.set_defaults(func=m3ut_show)

parser.add_argument('-d', '--directory', default='~/Music', help='Root directory to save merged m3u file.')
parser.add_argument('-n', '--dry-run', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-s', '--tree-suffix', default='.part')
parser.add_argument('-p', '--tree-prefix', default='')

args = parser.parse_args()
args.func(args)
