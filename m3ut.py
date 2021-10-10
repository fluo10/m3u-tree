#! /usr/bin/python3
import sys
import argparse
import os
import re
import glob

# import file
# for dir in file:
#     targetDirs.append(dir)

#m3u_pattern =  re.compile('(?P<hidden_prefix>\.|)(?P<playlist_name>.*)\.m3u')

class Playlist:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.tracks = set()
    def read_tracks(self, rootdir = ''):
        f = open(self.path, 'r', errors='replace')
        while True:
            line = f.readline().rstrip()
            if line == '':
                break

            if os.path.isabs(line):
                abspath = line
            else: 
                abspath = os.path.abspath(os.path.join( \
                    os.path.dirname(self.path), line))
            if rootdir == '':
                path = abspath
            else:
                path = os.path.relpath(abspath, rootdir)
            self.tracks.add(path)
        f.close()
        
    def write_tracks(self):
        dir = os.path.dirname(self.path)
        f = open(self.path, 'w')
        lines = map(lambda x: x + "\n", self.tracks)
        f.writelines(lines)
        f.close()
    def add_track(self,path):
        self.tracks.add(path)

    def compare(self, another):
        if args.verbose :
            print('compare')
    def exists(self):
        return os.path.isfile(self.path)

    def is_branch(self):
        return os.path.basename(self.path).removesuffix('.m3u') != self.name
    def show_summary(self, prefix):
        text = prefix + self.path
        count = len(self.tracks)
        if count > 0:
            count_str = '(' + str(count) + ')'
        else :
            count_str = '' 
        print(prefix + self.path + count_str)

#    def write_content(self):

class PlaylistTree:
    def __init__(self, name):
        self.name = name
        self.root_playlist = None
        self.branch_playlists = []
        self.branch_tracks = set()
#    def read_contents(self):
    def read_tracks(self, rootdir = ''):
        if not self.root_playlist is None: 
            self.root_playlist.read_tracks(rootdir)
        for playlist in self.branch_playlists:
            playlist.read_tracks(rootdir)
            self.branch_tracks = self.branch_tracks |  playlist.tracks


    def show(self):
        print(self.name)
        if len(self.branch_tracks) > 0 :
            count_str = '(' + str(len(self.branch_tracks)) + ')'
        else :
            count_str = ""
        print ('  root: ')
        if self.root_playlist is None:
            print('    None')
        else:
            print('    ' + self.root_playlist.path)
        
        print('  branches' + count_str + ':')
        for branch in self.branch_playlists:
            branch.show_summary('    ')
        print('')

    def diff(self):
        print(self.name)
        if self.root_playlist is None:
            root_tracks = set()
        else: 
            root_tracks = self.root_playlist.tracks
        

        # Tracks to keep
        print('  Keep:')
        for track in self.branch_tracks & root_tracks:
            print('    ' + track)


        # Tracks to add
        print('  Add:')
        for track in self.branch_tracks - root_tracks:
            print('    ' + track)
        
        # Tracks to delete
        print('  Delete:')
        for track in root_tracks - self.branch_tracks:
            print('    ' + track)
    def join(self):
        if self.root_playlist is None:
            self.root_playlist = Playlist(os.path.join(args.library_path, args.playlist_dirname, self.name + '.m3u'),self.name)
        
        self.root_playlist.tracks = self.branch_tracks
        self.root_playlist.write_tracks()

class PlaylistTrees:
    def __init__(self, args):
        self.root = args.library_path
        self.prefix = args.tree_prefix
        self.suffix = args.tree_suffix
        self.tree_dict = None
        self.reflesh_list()
        self.read_tracks()

    def reflesh_list(self):
        if not os.path.isdir(self.root):
            print('Error: ' + self.root + ' is not directory')

        self.tree_dict = {}
        for root, dirs, files in os.walk(self.root):
            for name in files:
                self.parse_tree_dict(os.path.join(root, name))

    def read_tracks(self):
        for tree in self.tree_dict.values():
            tree.read_tracks(self.root)

    def parse_tree_dict(self, path):
        dir = os.path.dirname(path)
        
        file = os.path.basename(path)
        if (not(file.startswith(self.prefix) and file.endswith(self.suffix))) and (not (file.endswith('.m3u') and os.path.samefile(dir, os.path.join(self.root, args.playlist_dirname)))):
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
    def diff(self):
        for tree in self.tree_dict.values():
            tree.diff()

    def join(self):
        for tree in self.tree_dict.values():
            tree.join()

playlist_dict = {}


def m3ut_join(args):
    print('m3u-tools join')
    PlaylistTrees(args).join()

def m3ut_show(args):
    print('m3u-tools show')
    print(PlaylistTrees(args).show())

def m3ut_diff(args):
    PlaylistTrees(args).diff()

def m3ut_check(args):
    print('m3u-tools check')
    print(load_m3u(args.library_path))

def m3ut_split(args):
    print('m3u-tools split')

def m3ut_fix(args):
    print('m3u-tools fix')

def m3ut_add_track(args):
        
    for track in args.tracks:
        if os.path.isfile(track):
            track_path = track
        else:
            tmp = glob.glob(track + '*')
            if len(tmp) == 1:
                track_path = tmp[0]
            else:
                print('Track "' + track + '" is not one track')
                continue    
        for playlist_name in args.playlists:
            if os.path.dirname(playlist_name) == '':
                playlist_path = os.path.join(os.path.dirname(track_path), playlist_name)
            else:
                playlist_path = playlist_name
            playlist = Playlist(playlist_path, os.path.basename(playlist_path))
            playlist.add_track(track_path)
            playlist.write_tracks()
            print('Add "' + track_path + '" to "' + playlist_path + '"')

    

parser = argparse.ArgumentParser(description='Merging same name m3u files')
subparsers = parser.add_subparsers(help='sub-command help')

parser_join = subparsers.add_parser('join', help='Join playlists with the same name')
parser_join.set_defaults(func=m3ut_join)

parser_check = subparsers.add_parser('check', help='Check playlists')
parser_check.set_defaults(func=m3ut_check)

parser_split = subparsers.add_parser('split', help='Split playlists to each directory including tracks')
parser_split.set_defaults(func=m3ut_split)

parser_fix = subparsers.add_parser('fix', help='Fix path of missing tracks')
parser_fix.set_defaults(func=m3ut_fix)

parser_show = subparsers.add_parser('show', help='Show list of playlist')
parser_show.set_defaults(func=m3ut_show)

parser_show = subparsers.add_parser('diff', help='Show differences of track between branch and root')
parser_show.set_defaults(func=m3ut_diff)

# parser_branch = subparsers.add_parser('branch', help='Managing branch playlists')
# branch_subparsers = parser_branch.add_subparsers(help='branch sub-command help')
# branch_subparsers.add_parser('Add')

# Set common arguments
for subparser in subparsers.choices.values():
    subparser.add_argument('-l', '--library-path', default='~/Music', help='Target music library')
    subparser.add_argument('-p', '--playlist-dirname', default='Playlists', help='Directory name to save joined playlists')
    subparser.add_argument('-n', '--dry-run', action='store_true')
    subparser.add_argument('-v', '--verbose', action='store_true')
    subparser.add_argument('-s', '--tree-suffix', default='.part', help='Suffic to determine whether branch playlist')
    subparser.add_argument('-P', '--tree-prefix', default='', help='Prefix to determine whether branch playlist')

parser_add_track = subparsers.add_parser('add-track', help='Add track to branch playlist')
parser_add_track.set_defaults(func=m3ut_add_track)
parser_add_track.add_argument('-p', '--playlists', nargs='*', help='Target playlist')
parser_add_track.add_argument('-t', '--tracks', nargs='*', help='Target tracks')
parser_add_track.add_argument('-s', '--tree-suffix', default='.part', help='Suffic to determine whether branch playlist')
parser_add_track.add_argument('-P', '--tree-prefix', default='', help='Prefix to determine whether branch playlist')

args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()
