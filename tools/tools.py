#!/usr/local/bin/kivy

import kivy
import sys

kivy.require('1.7.1')

from os.path import join, abspath, isdir, basename
from os import walk, chdir
from glob import glob
from kivy.atlas import Atlas


def create_atlas(args):
    ''' Parse sub-directories in src and creates the kivy:atlas compliant stuff in dst
    '''
    try:
        src = args.src or '.'
        dst = args.dst or '..'

        if not isdir(src):
            raise Exception('source `%s` is not a directory!' % src)
        if not isdir(dst):
            raise Exception('destination `%s` is not a directory' % dst)

        for folder in list(abspath(f) for f in glob(join(src, '*'))):
            if not isdir(folder):
                print 'skipping %s (not a folder)' % folder
            continue

        print 'Processing folder %s' % folder

        images = []
        for root, dirname, filenames in walk(folder):
            for filename in filenames:
                image = join(root, filename)[len(folder) + 1:]
                print image
                images.append(image)

        chdir(folder)
        Atlas.create(join(dst, basename(folder)), images, args.size, use_path=True)

    except Exception, e:
        print e


def main(argv=None):
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Create kivy atlases')
    parser.add_argument('--dst', help='destination')
    parser.add_argument('--src', help='source folder (where atlas sub-folders reside)')
    parser.add_argument('--size', type=int, default=512, help='atlas texture size')
    args = parser.parse_args(argv[1:])

    create_atlas(args)

if __name__ in '__main__':
    main()

