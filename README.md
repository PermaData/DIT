DIT
___

## About

The primary target users of DIT are field scientists focuses on the collection of in situ data in the field.  The initial focus is on permafrost scientists who collect borehole data, but the full target user group is all field scientists.  One secondary target user group of DIT is modelers who use data for model input or validation.  The initial focus is on permafrost modelers, but the full target user group is the entire physical modeling community.  Another secondary target user group is non-discipline scientists, who are analyzing data collected by others in a different scientific discipline.

All users face the exact same problem: how to process data into a structure and format so that they can use it.  The data can come from multiple sources with different data structures, units and nomenclature.  Each user application is unique, so how they process the data is also unique.  The time and effort required to process data is the single largest barrier to data reuse.

## Overview

The Data Integration Tool (DIT) consists of:

*   dit_flow is available as a command line tool has 2 main parts:
   + a [circuits](http://circuitsframework.com) based workflow manager
   + dit_widget - an extendable collection of single operation widgets designed to be chained together to create a data manipulation workflow.
* dit_gui - a graphical user interface that creates dit flows which interact with dit_flow.
* dit_core - the original Fortran based tool.

___
## Installation
### 64-bit Linux/unix
#### Requirements:
* writable directory
* installed curl package
* installed unzip package

From within a writable directory, run the following command:
``` html
curl -L http://bit.ly/2j2SZz3 | bash
```

## Testing DIT
From within the DIT-master directory, run the tests:
``` html
$ inv test
```

## Running DIT
### Example Run on Linux
From within the DIT-master directory, run the following commands:
``` html
$ source env.sh
```
* Should see the following output...
``` html
Adding conda to your path...
Activating dit conda environment...
All done. Enjoy!
```

``` html
$ python run_flow.py example/example_config.yml -l run_flow.log
```
* Should see similar log output to the following:
``` html
directory:  /projects/MULTIMOD/PermaData/dit-circuits
widget directory:  /projects/MULTIMOD/PermaData/dit-circuits/dit_flow/dit_widget
flow dir:  /projects/MULTIMOD/PermaData/dit-circuits/dit_flow
2017-10-02 10:31:33,360 : Setup logging into: log.file
2017-10-02 10:31:33,361 : Loading configuration file: example/example_config.yml
2017-10-02 10:31:33,361 : Loading configuration file: example/example_config.yml
2017-10-02 10:31:33,369 : Setting up file manager widget
2017-10-02 10:31:33,379 : Setting up reader widget: read_csv_file
2017-10-02 10:31:33,395 : Setting up variable mapper widget
2017-10-02 10:31:33,405 : Setting up writer widget: write_csv_file
```

___
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


