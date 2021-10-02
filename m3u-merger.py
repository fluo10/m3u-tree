#! /usr/bin/python3
import sys
import argparse
import os
import re

parser = argparse.ArgumentParser(description='Merging same name m3u files')
parser.add_argument('-d', '--directory', nargs='*', help='Root directory to save merged m3u file.')
parser.add_argument('-f', '--file', help='File saving list of directory')
parser.add_argument('-n', '--dry-run', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
print(args.dry_run)

targetDirs = []
for dir in args.directory:
    targetDirs.append(dir)

# import file
# for dir in file:
#     targetDirs.append(dir)

m3u_pattern = re.compile('.*\.m3u')
hidden_m3u_pattern =  re.compile('\..*\.m3u')

class MyPlaylist:
    def __init__(self, name):
        self._name = name
        self._tracks = []
    def add_track(self, track):
        self._tracks.append(track)
    def import_m3u(self, file):
        if args.verbose :
            print('import file')
    def compare(self, another):
        if args.verbose :
            print('compare')

def compile_m3u(targetDirPath):
    
    if not os.path.isdir(targetDirPath):
        print('Error: ' +targetDirPath + ' is not directory')

    for dirPath, dirList, fileList in os.walk(targetDirPath):
        # print(dirPath)
        for fileName in fileList:
            if hidden_m3u_pattern.fullmatch(fileName) :
                if args.verbose :
                    print(fileName)


for dir in targetDirs:
    compile_m3u(dir)

print('End script')
