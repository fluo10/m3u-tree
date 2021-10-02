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
    def __init__(self, path):
        self.path = path
        self.tracks = []
    def add_track(self, track):
        self.tracks.append(track)
    def import_m3u(self, file):
        if args.verbose :
            print('import file')
    def compare(self, another):
        if args.verbose :
            print('compare')
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
    def __init__(self, rootdir):
        self.root = rootdir 
        self.reflesh()
    def reflesh(self):
        m3u_path_list = show_m3u(self.root)
        self.tree_dict = {}
        for path in m3u_path_list:
            m3u_match = m3u_pattern.fullmatch(os.path.basename(path))
            m3u_groupdict = m3u_match.groupdict()
            playlist_name = m3u_groupdict.get('playlist_name')
            hidden = (m3u_groupdict.get('hidden_prefix') == '.')
            if not (playlist_name in self.tree_dict):
                self.tree_dict[playlist_name] = PlaylistTree(playlist_name)
            tree = self.tree_dict.get(playlist_name)
            
            if os.path.samefile(os.path.dirname(path), self.root):
                tree.root_playlist = Playlist(path)
            elif hidden :
                tree.branch_playlists.append(Playlist(path))
            
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
    print(PlaylistTrees(args.directory).show())

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

args = parser.parse_args()
args.func(args)
