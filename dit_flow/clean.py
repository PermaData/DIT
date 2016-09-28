import os
import shutil

def rm_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

def clean():
    rm_dir('build')
    rm_dir('dist')
    rm_dir('dit_widget.egg-info')
#    rm_dir('rill/rill.egg-info')
#    rm_dir('rill/build')
#    rm_dir('rill/dist')

if __name__ == '__main__':
    clean()
