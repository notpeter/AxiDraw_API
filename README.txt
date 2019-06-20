Stand-alone command line interface and python API
for the AxiDraw writing and drawing machine.

Supported on python 2.7, python 3.6, Mac, Windows, and Linux.


Copyright 2018 Evil Mad Scientist Laboratories

The AxiDraw writing and drawing machine is a product of Evil Mad Scientist
Laboratories. https://axidraw.com   https://shop.evilmadscientist.com


----------


Please see Installation.txt for requirements.


----------

This directory contains the following items:

axicli.py               - The command line interface (CLI) program itself

pyaxidraw/              - The AxiDraw python package directory

Installation.txt        - Installation documentation

python_example_plot.py  - Example files, showing use of this software
python_example_xy.py	  as a python module, to plot an SVG file or to
                          execute XY motion commands

AxiDraw_trivial.svg     - Sample SVG file that can be plotted


----------

COMMAND LINE INTERFACE: USAGE

For detailed documentation, please refer to:
    
    https://axidraw.com/doc/cli_api/


Quick start (CLI): 

(1) To plot an SVG document called "AxiDraw_trivial.svg" from the command line,
    use the AxiDraw CLI:

        python axicli.py AxiDraw_trivial.svg


(2) The CLI features an extensive set of control options. For quick help, use: 

        python axicli.py --help

----------
    
PYTHON API: USAGE

For detailed documentation, please refer to:
    
    https://axidraw.com/doc/py_api/
    
Quick Start:

(1) The file "python_example_plot.py" is an example python script, showing how
one can use a the axidraw python module in "plot" mode to open and plot an SVG
file. 

    To run the example, call:

        python python_example_plot.py

    This is a minimal demonstration script for opening and plotting an SVG file
    (in this case, "AxiDraw_trivial.svg") from within a python script. 


(2) The file "python_example_xy.py" is an example python script, showing how one
can use a the axidraw python module in "interactive" mode, to execute absolute
and relative XY motion control commands like move(x,y), lineto(x,y), penup()
and pendown(). 

    To run the example, call:

        python python_example_xy.py




----------
    

Licensing:

The AxiDraw CLI and top level example scripts are licensed under the MIT license. 
Some of the underlying libraries that are included with this distribution
(including those forked from the Inkscape project) are licensed as GPL, and pyserial is under a BSD license. Please see the individual files and directories included with this distribution for additional license information. 

API Documentation: Copyright 2018, Windell H. Oskay, Evil Mad Scientist Laboratories.



