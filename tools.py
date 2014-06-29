import kivy

kivy.require('1.7.1')

from os.path import join, abspath, isdir, basename
from os import walk, chdir
from glob import glob
from kivy.atlas import Atlas

DEFAULT_SIZE = 512
FOLDER_MASK = '*'

"""
this parses sub-directories in cwd and creates the kivy:atlas compliant stuff
"""
def create_atlas(argv=None):
    try:
        for folder in list(abspath(f) for f in glob(FOLDER_MASK)):
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
        Atlas.create(join('..', basename(folder)), images, DEFAULT_SIZE, use_path=True)

    except Exception, e:
        print e


if __name__ in '__main__':
    create_atlas()