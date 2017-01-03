import os
from distutils.core import run_setup
from setuptools import setup, find_packages

os.chdir('./rill')
run_setup('setup.py', ['install'])
os.chdir('..')

setup(name='dit_widget',
      version='0.0.0.dev1',
      description='Data Integration Tool (DIT) designed to help debug data transformation.',
      url='http://github.com/PermaData/dit',
      author='National Snow and Ice Data Center',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.5',
      ],
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
