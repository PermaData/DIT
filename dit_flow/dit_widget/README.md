DIT WIDGET
=====================

## About
Standard and custom widgets that perform operations for the DIT application.

These widgets are also setup as rill components to be used by the rill
application.

## Overview
*   dit_flow is a command line tool has 2 main parts:
   + rill - a fork of the Flow-Based Programming (FBP) python tool rill we are using as a workflow manager
   + dit_widget - an extendable collection of single operation widgets (rill components) designed to be chained together to create a data manipulation workflow.

## Installation
dit_widget and rill are both designed to be installed as python
packages. rill has been added as a submodule in the 'rill' directory. To
setup your environment for development:
* Clone the DIT repository recursively:
  'git clone --recursive https://github.com/PermaData/DIT.git'
  or clone regularly and initialize and update submodules
  'git clone https://github.com/PermaData/DIT.git',
  then 'git submodule init', then 'git submodule update'
* Setup your python 3 environment and pip install the requirements from
  dit_flow/requirements.txt and dit_flow/rill/requirements.txt
* In the dit_flow directory run the following to install the dit_widget
  package in develop mode and the rill package built from the rill
  directory: 'python setup develop'

If you want to rebuild and redeploy the dit_widget and rill packages:
* Uninstall existing dit_widget and rill with:
  'pip uninstall dit_widget'
  'pip uninstall rill'
* Clean the package builds. From dit_flow run: 'python clean.py'
* Rebuild and install packages. From dit_flow run: 'python setup.py
  develop'

## Credit

This software was developed by the National Snow and Ice Data Center under NSF award number 1416712.

## LICENSE

Copyright (c) 2016 Regents of the University of Colorado

This software was developed by the National Snow and Ice Data Center under NSF award number 1416712.

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
