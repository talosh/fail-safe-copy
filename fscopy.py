#!/usr/bin/python

import os
import sys
import argparse
import subprocess

from pprint import pprint, pformat

parser = argparse.ArgumentParser(description='Failsafe copy')
parser.add_argument('source', help='source folder or list of file paths to copy')
parser.add_argument('destination', help='destination folder')
parser.add_argument('--fileslist', dest='flist', action='store_true', help='treat first argument as list of files')
args = parser.parse_args()

if args.flist:
    try:
        f = open(args.source, 'r')
        file_list = f.read()
        f.close()
    except Exception as e:
        pprint (e)
        sys.exit()
else:
    cmd_find = [
            'find',
            args.source,
            '-type', 'f',
            ]

    file_list = subprocess.check_output(cmd_find)

if not os.path.isdir(args.destination):
    try:
        cmd = 'mkdir -p ' + args.destination
        os.system(cmd)
    except Exception as e:
        pprint (e)
        sys.exit()

file_list = file_list.split('\n')
file_list = sorted(file_list)

for file_path in file_list:
    if not file_path:
        continue
    if not os.path.isfile(file_path):
        continue
    
    dest_folder = os.path.join(
        args.destination,
        os.path.dirname(file_path)[1:]
    )

    try:
        cmd = 'mkdir -p ' + dest_folder
        os.system(cmd)
    except Exception as e:
        pprint (e)
        continue

    if not os.path.isdir(dest_folder):
        print ('destination does not exists: %s' % dest_folder)
        print ('skipping...')
        continue
    
    dest_path = os.path.join(
        dest_folder,
        os.path.basename(file_path)
    )

    if os.path.isfile(dest_path):
        print ('file %s already exists, skipping...' % dest_path)

    print ('copying %s' % dest_path)
    try:
        cmd = 'dd if=' + file_path + ' of=' + dest_path + ' conv=sync,noerror'
        os.system(cmd)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        pprint (e)
        continue


