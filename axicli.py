#!/usr/bin/env python
# -*- encoding: utf-8 -#-

from __future__ import print_function

'''
axicli.py   - Command line interface (CLI) for AxiDraw.

For quick help:
    python axicli.py --help

Full user guide:  
    https://axidraw.com/doc/cli_api/


This script is a stand-alone version of AxiDraw Control, accepting 
various options and providing a facility for setting default values.

'''


'''
About this software:

The AxiDraw writing and drawing machine is a product of Evil Mad Scientist
Laboratories. https://axidraw.com   https://shop.evilmadscientist.com

This open source software is written and maintained by Evil Mad Scientist
to support AxiDraw users across a wide range of applications. Please help
support Evil Mad Scientist and open source software development by purchasing
genuine AxiDraw hardware.

AxiDraw software development is hosted at https://github.com/evil-mad/axidraw

Additional AxiDraw documentation is available at http://axidraw.com/docs

AxiDraw owners may request technical support for this software through our 
github issues page, support forums, or by contacting us directly at:
https://shop.evilmadscientist.com/contact



Copyright 2018 Windell H. Oskay, Evil Mad Scientist Laboratories

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import sys
import os
import argparse

cli_version = "AxiDraw Command Line Interface v2.3.0 (beta)"

def quickhelp():
    
    main_text = '''
    (c) 2018 Evil Mad Scientist Laboratories
         
    Basic syntax to plot a file: 
        python axicli.py [options] filename.svg
    
    For a quick list of options, use:
        python axicli.py --help

    To read the full manual, please see:
        https://axidraw.com/doc/cli_api/'''
    
    return cli_version + main_text


def axidraw_CLI():
    
    desc = 'AxiDraw Command Line Interface.'

    parser = argparse.ArgumentParser(description=desc, usage=quickhelp())
    
    parser.add_argument("inputfile", \
            help="The SVG file to be plotted")

    parser.add_argument("-m","--mode", \
             metavar='MODENAME', type=str, \
             help="Mode. One of: [plot, layers, align, toggle, manual, " \
             + "sysinfo, version, res_plot, res_home, reorder]. Default: plot.")

    parser.add_argument("-s","--speed_pendown", \
            metavar='SPEED',  type=int, \
            help="Maximum plotting speed, when pen is down (1-100)")
            
    parser.add_argument("-S","--speed_penup", \
            metavar='SPEED', type=int, \
            help="Maximum transit speed, when pen is up (1-100)")
            
    parser.add_argument("-a","--accel", \
            metavar='RATE', type=int, \
            help="Acceleration rate factor (1-100)")

    parser.add_argument("-d","--pen_pos_down", \
            metavar='HEIGHT', type=int, \
            help="Height of pen when lowered (0-100)")
            
    parser.add_argument("-u","--pen_pos_up", \
            metavar='HEIGHT', type=int,  \
            help="Height of pen when raised (0-100)")
            
    parser.add_argument("-r","--pen_rate_lower", \
            metavar='RATE', type=int, \
            help="Rate of lowering pen (1-100)")
    
    parser.add_argument("-R","--pen_rate_raise", \
            metavar='RATE', type=int, \
            help="Rate of raising pen (1-100)")
            
    parser.add_argument("-z","--pen_delay_down", \
            metavar='DELAY',type=int, \
            help="Optional delay after pen is lowered (ms)")
            
    parser.add_argument("-Z","--pen_delay_up", \
            metavar='DELAY',type=int, \
            help="Optional delay after pen is raised (ms)")

    parser.add_argument("-N","--no_rotate", \
            action="store_true",\
            help="Disable auto-rotate; preserve plot orientation")
            
    parser.add_argument("-C","--const_speed",\
            action="store_true",\
            help="Use constant velocity when pen is down")
            
    parser.add_argument("-T","--report_time", \
            action="store_true", \
            help="Report time elapsed")

    parser.add_argument("-M","--manual_cmd", \
            metavar='COMMAND', type=str, \
            help="Manual command. One of: [ebb_version, lower_pen, raise_pen, "\
            + "walk_x, walk_y, enable_xy, disable_xy, bootload, strip_data, " \
            + "read_name, list_names,  write_name]. Default: ebb_version")
            
    parser.add_argument("-w","--walk_dist", \
            metavar='DISTANCE', type=float, \
            help="Distance for manual walk (inches)")
    
    parser.add_argument("-l","--layer", \
            type=int, \
            help="Layer(s) selected for layers mode (1-1000). Default: 1")
            
    parser.add_argument("-c","--copies", \
            metavar='COUNT', type=int, \
            help="Copies to plot, or 0 for continuous plotting. Default: 1")

    parser.add_argument("-D","--page_delay", \
             metavar='DELAY', type=int,\
             help="Optional delay between copies (s).")

    parser.add_argument("-v","--preview", \
            action="store_true", \
            help="Preview mode; simulate plotting only.")

    parser.add_argument("-g","--rendering", \
            metavar='RENDERCODE', type=int, \
            help="Preview mode rendering option (0-3). 0: None. " \
            + "1: Pen-down movement. 2: Pen-up movement. 3: All movement.")

    parser.add_argument("-G","--group_sorting", \
            metavar='GROUP_CODE', type=int, \
            help="SVG sorting group handling option (0-2). 0: Preserve. " \
            + "1: Sort within groups. 2: Break apart. Default: 1")

    parser.add_argument("-L","--model",\
            metavar='MODELCODE', type=int,\
            help="AxiDraw Model (1-3). 1: AxiDraw V2 or V3. " \
            + "2:AxiDraw V3/A3. 3: AxiDraw V3 XLX.")

    parser.add_argument("-p","--port",\
            metavar='PORTNAME', type=str,\
            help="Serial port or named AxiDraw to use")
 
    parser.add_argument("-P","--port_config",\
            metavar='PORTCODE', type=int,\
            help="Port use code (0-3)."\
            +" 0: Plot to first unit found, unless port is specified"\
            + "1: Plot to first AxiDraw Found. "\
            + "2: Plot to specified AxiDraw. "\
            + "3: Plot to all AxiDraw units. ")

    parser.add_argument("-o","--output_file",\
            metavar='FILE', \
            help="Optional SVG output file name")
 
 
    args = parser.parse_args()
    
    # Handle trivial cases:
    
    if args.inputfile == "help":
        print(quickhelp())
        quit()

    if args.inputfile == "version":
        from pyaxidraw import axidraw
        ad = axidraw.AxiDraw()
        print (cli_version)
        print (ad.version_string)
        quit()

    if args.mode == "options":
        quit()
        
    if args.mode == "timing":
        quit()    

    if not os.path.isfile(args.inputfile):
        # If the input file does not exist, return an error.
        print("Input file not located. For help, try:")
        print("    python axicli.py --help")
        quit()

    if args.mode == "reorder":
        from pyaxidraw import axidraw_svg_reorder

        adc = axidraw_svg_reorder.ReorderEffect()

        adc.getoptions([])
        adc.parse(args.inputfile)

        if args.rendering is not None:
            if args.rendering > 1:
                adc.options.rendering = True

        if args.group_sorting is not None:
            adc.options.group_handling = args.group_sorting

        print("Re-ordering SVG File.")
        print("This can take a while for large files.")
        
        adc.effect()    # Sort the document

        if args.output_file:
            writeFile = open(args.output_file,'w')         # Open output file for writing.
            writeFile.write(adc.get_output())
            writeFile.close()
        print("Done")

        quit()


    # For nontrivial cases, import the axidraw module and go from there:

    from pyaxidraw import axidraw_control

    adc = axidraw_control.AxiDrawWrapperClass()

    adc.getoptions([])
    adc.parseFile(args.inputfile)
    
    # Pass through each parameter that has been specified.
    # Do NOT pass through parameters that are not specified;
    #   That will ensure that they are properly given default values.
    
    if args.mode is not None:
        adc.options.mode = args.mode

    if args.speed_pendown is not None:
       adc.options.speed_pendown = args.speed_pendown

    if args.speed_penup is not None:
       adc.options.speed_penup = args.speed_penup
       
    if args.accel is not None:
        adc.options.accel = args.accel
        
    if args.pen_pos_down is not None:
       adc.options.pen_pos_down = args.pen_pos_down

    if args.pen_pos_up is not None:
       adc.options.pen_pos_up = args.pen_pos_up

    if args.pen_rate_lower is not None:
       adc.options.pen_rate_lower = args.pen_rate_lower

    if args.pen_rate_raise is not None:
       adc.options.pen_rate_raise = args.pen_rate_raise

    if args.pen_delay_down is not None:
      adc.options.pen_delay_down = args.pen_delay_down

    if args.pen_delay_up is not None:
       adc.options.pen_delay_up = args.pen_delay_up

    if args.no_rotate is not None:
       adc.options.no_rotate = args.no_rotate
       
    if args.const_speed is not None:
       adc.options.const_speed = args.const_speed
       
    if args.report_time is not None:
      adc.options.report_time = args.report_time
      
    if args.manual_cmd is not None:
      adc.options.manual_cmd = args.manual_cmd
      
    if args.walk_dist is not None:
       adc.options.walk_dist = args.walk_dist
       
    if args.layer is not None:
       adc.options.layer = args.layer

    if args.copies is not None:
       adc.options.copies = args.copies
  
    if args.page_delay is not None:
       adc.options.page_delay = args.page_delay 

    if args.preview is not None:
       adc.options.preview = args.preview
       
    if args.rendering is not None:
       adc.options.rendering = args.rendering
       
    if args.model is not None:
       adc.options.model = args.model
       
    if args.port is not None:
        adc.options.port = args.port
        
    if args.port_config is not None:
        adc.options.port_config = args.port_config 

#     The following options are deprecated and should not be used.
#     adc.options.setup_type          = args.setup_type  # Legacy input; not needed
#     adc.options.smoothness          = args.smoothness  # Legacy input; not needed
#     adc.options.cornering           = args.cornering   # Legacy input; not needed
#     adc.options.resolution          = args.resolution  # Legacy input; not needed
#     adc.options.resume_type         = args.resume_type # Legacy input; not needed
#     adc.options.auto_rotate         = args.auto_rotate # Legacy input; not needed

    adc.effect()    # Plot the document

    if args.output_file:
        writeFile = open(args.output_file,'w')         # Open output file for writing.
        writeFile.write(adc.outdoc)
        writeFile.close()

if __name__ == '__main__':
    axidraw_CLI()
