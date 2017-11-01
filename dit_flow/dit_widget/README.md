DIT WIDGET
=====================

## About
Standard and custom widgets that perform operations for the DIT application.

These widgets are also setup as circuits components that can be used the
[circuits](http://circuitsframework.com) framework.

## Overview
*   dit_flow is a command line tool
   + dit_widget - an extendable collection of single operation widgets designed to be chained together to create a data manipulation workflow.

## Installation
dit is designed to be installed as python a package.
To setup your environment for development:
* Clone the DIT repository recursively:
  `git clone https://github.com/PermaData/DIT.git`
* Create the conda environment (assumes you have conda installed):
  `conda env create -f environment.yml`
* In the dit_flow directory run the following to install dit as a package in development mode:
  `python setup develop`

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
