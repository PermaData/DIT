from setuptools import setup, find_packages

setup(name='dit',
      version='0.0.0.dev1',
      description='Data Integration Tool (DIT) designed to help debug data transformation.',
      url='https://github.com/PermaData/DIT',
      author='National Snow and Ice Data Center',
      license='GPLv3',
      packages=find_packages(exclude=('tasks', 'dit_core')))
