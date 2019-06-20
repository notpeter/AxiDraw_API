# axidraw_merge.py
# Part of the AxiDraw driver for Inkscape
# https://github.com/evil-mad/AxiDraw
#
# See versionString below for detailed version number.
#
# Copyright 2018 Windell H. Oskay, Evil Mad Scientist Laboratories
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Requires Pyserial 2.7.0 or newer. Pyserial 3.0 recommended.


import sys

import os

from axidrawimport import from_ink_extensions_import
inkex = from_ink_extensions_import('inkex')

import time
import csv
from re import sub, compile, escape
from StringIO import StringIO
import gettext
from lxml import etree


import axidraw_merge_conf    #Some settings can be changed here.
import ebb_serial    # Requires v 0.9 in plotink:     https://github.com/evil-mad/plotink
import ebb_motion    # Requires v 0.11 in plotink


class AxiDrawMergeClass( inkex.Effect ):

    def __init__( self ):
        inkex.Effect.__init__( self )




        self.OptionParser.add_option("--mode",\
            action="store", type="string", dest="mode",\
            default="autoPlot", \
            help="Mode or GUI tab. One of: [autoPlot, singlePlot, csv, setup, "\
            + "options, model, timing, text, version]. Default: autoPlot.")
            
        self.OptionParser.add_option( "--firstRow", action="store", type="int", dest="first_row", default=axidraw_merge_conf.firstRow, help="Merge Start Row." )
        self.OptionParser.add_option( "--lastRow", action="store", type="int", dest="last_row", default=axidraw_merge_conf.lastRow, help="Merge End Row." )

        self.OptionParser.add_option( "--singleType", action="store", type="string", dest="single_type", default="singleFix", help="The type of single-page plot to use" )
        self.OptionParser.add_option( "--singleRow", action="store", type="int", dest="single_row", default=axidraw_merge_conf.singleRow, help="Specified Row to Merge" )

        self.OptionParser.add_option( "--dataAction", action="store", type="string", dest="data_action", default="choose", help="Choose, view, or erase CSV data" )

        self.OptionParser.add_option( "--fontface", action="store", type="string", dest="fontface", default=axidraw_merge_conf.fontface, help="The selected font face when Apply was pressed" )
        self.OptionParser.add_option( "--letterSpacing", action="store", type="int", dest="letter_spacing", default=axidraw_merge_conf.letterSpacing, help="Override letter spacing " )
        self.OptionParser.add_option( "--wordSpacing", action="store", type="int", dest="word_spacing", default=axidraw_merge_conf.wordSpacing, help="Override word spacing " )            
        self.OptionParser.add_option( "--enableDefects", action="store", type="inkbool", dest="enable_defects", default=axidraw_merge_conf.enableDefects, help="Enable Handwriting Defects")            
        self.OptionParser.add_option( "--baselineVar", action="store", type="int", dest="baseline_var", default=axidraw_merge_conf.baselineVar, help="Variation in baseline Jitter" )
        self.OptionParser.add_option( "--indentVar", action="store", type="int", dest="indent_var", default=axidraw_merge_conf.indentVar, help="Variation in indent " )
        self.OptionParser.add_option( "--kernVar", action="store", type="int", dest="kern_var", default=axidraw_merge_conf.kernVar, help="Variation in letter kerning " )
        self.OptionParser.add_option( "--sizeVar", action="store", type="int", dest="size_var", default=axidraw_merge_conf.sizeVar, help="Variation in font size " )


        self.OptionParser.add_option("--speed_pendown",\
            type="int", action="store", dest="speed_pendown", \
            default=axidraw_merge_conf.speed_pendown, \
            help="Maximum plotting speed, when pen is down (1-100)")
            
        self.OptionParser.add_option("--speed_penup",\
            type="int", action="store", dest="speed_penup", \
            default=axidraw_merge_conf.speed_penup, \
            help="Maximum transit speed, when pen is up (1-100)")
        
        self.OptionParser.add_option("--accel",\
            type="int", action="store", dest="accel", \
            default=axidraw_merge_conf.accel, \
            help="Acceleration rate factor (1-100)")

        self.OptionParser.add_option("--pen_pos_up",\
            type="int", action="store", dest="pen_pos_up", \
            default=axidraw_merge_conf.pen_pos_up, \
            help="Height of pen when raised (0-100)")

        self.OptionParser.add_option("--pen_pos_down",\
            type="int", action="store", dest="pen_pos_down",\
            default=axidraw_merge_conf.pen_pos_down,\
            help="Height of pen when lowered (0-100)")
        
        self.OptionParser.add_option("--pen_rate_raise",\
            type="int", action="store", dest="pen_rate_raise",\
            default=axidraw_merge_conf.pen_rate_raise,\
            help="Rate of raising pen (1-100)")
         
        self.OptionParser.add_option("--pen_rate_lower",\
            type="int", action="store", dest="pen_rate_lower",\
            default=axidraw_merge_conf.pen_rate_lower, \
            help="Rate of lowering pen (1-100)")
        
        self.OptionParser.add_option("--pen_delay_up",\
            type="int", action="store", dest="pen_delay_up", \
            default=axidraw_merge_conf.pen_delay_up,\
            help="Optional delay after pen is raised (ms)")
           
        self.OptionParser.add_option("--pen_delay_down",\
            type="int", action="store", dest="pen_delay_down",\
            default=axidraw_merge_conf.pen_delay_down,\
            help="Optional delay after pen is lowered (ms)")

        self.OptionParser.add_option("--no_rotate",\
            type="inkbool", action="store", dest="no_rotate",\
           default=False,\
           help="Disable auto-rotate; preserve plot orientation")
           # TODO: Add support for this option
           
        self.OptionParser.add_option("--const_speed",\
            type="inkbool", action="store", dest="const_speed",\
            default=axidraw_merge_conf.const_speed,\
            help="Use constant velocity when pen is down")
         
        self.OptionParser.add_option("--report_time",\
            type="inkbool", action="store", dest="report_time",\
            default=axidraw_merge_conf.report_time,\
            help="Report time elapsed")
        
        self.OptionParser.add_option("--page_delay",\
            type="int", action="store", dest="page_delay",\
            default=axidraw_merge_conf.page_delay,\
            help="Optional delay between copies (s).")

        self.OptionParser.add_option("--preview",\
            type="inkbool", action="store", dest="preview",\
            default=axidraw_merge_conf.preview,\
            help="Preview mode; simulate plotting only.")
            
        self.OptionParser.add_option("--rendering",\
            type="int", action="store", dest="rendering",\
            default=axidraw_merge_conf.rendering,\
            help="Preview mode rendering option (0-3). 0: None. " \
            + "1: Pen-down movement. 2: Pen-up movement. 3: All movement.")

        self.OptionParser.add_option("--model",\
            type="int", action="store", dest="model",\
            default=axidraw_merge_conf.model,\
            help="AxiDraw Model (1-3). 1: AxiDraw V2 or V3. " \
            + "2:AxiDraw V3/A3. 3: AxiDraw V3 XLX.")

        self.OptionParser.add_option("--port",\
            type="string", action="store", dest="port",\
            default=axidraw_merge_conf.port,\
            help="Serial port or named AxiDraw to use")
                        
        self.OptionParser.add_option("--port_config",\
            type="int", action="store", dest="port_config",\
            default=None,\
            help="Port use code (1-3). 1: First AxiDraw Found. " \
            + "2:AxiDraw at --port only.")

        self.OptionParser.add_option("--setup_type",\
            type="string", action="store", dest="setup_type",\
            default="align",\
            help="Setup option selected (GUI Only)")
            
        self.OptionParser.add_option("--resume_type",\
            type="string", action="store", dest="resume_type",\
            default="plot",
            help="The resume option selected (GUI Only)")

        self.OptionParser.add_option("--auto_rotate",\
            type="inkbool", action="store", dest="auto_rotate",\
            default=axidraw_merge_conf.auto_rotate,\
            help="Boolean: Auto select portrait vs landscape (GUI Only)")       

        self.OptionParser.add_option("--resolution",\
            type="int", action="store", dest="resolution",\
            default=axidraw_merge_conf.resolution,\
            help="Resolution option selected (GUI Only)")









    def effect( self ):
        '''Main entry point: check to see which mode/tab is selected, and act accordingly.'''

        self.versionString = "AxiDraw Merge - Version 2.0.0 dated 2018-07-10"
        self.spewDebugdata = False

        self.start_time = time.time()        
        self.pageDelays = 0.0
        self.rows_plotted = 0
        
        self.serial_port = None
        self.svg_data_written = False
        self.csv_data_read = False
        self.csv_data_written = False
        self.csv_file_path = None
        self.csv_row_count = None
        
        self.delay_between_rows = False    # Not currently delaying between copies
        self.b_stopped = False # Not currently stopped by button press
        
        #Values to be read from file:
        self.svg_rand_seed_Old = float( 1.0 )    
        self.svg_row_old = float( 0.0 )    # Last row plotted.
        self.svg_rand_seed = float( 1.0 )    
        self.svgRow = int( 1 )    

        self.row_to_plot = 1

        skipSerial = False
        if self.options.preview:
            skipSerial = True
        
        # Input sanitization:
        self.options.mode = self.options.mode.strip("\"")
        self.options.single_type = self.options.single_type.strip("\"")
        self.options.data_action = self.options.data_action.strip("\"")
        self.options.fontface = self.options.fontface.strip("\"")
        self.options.setup_type = self.options.setup_type.strip("\"")
        self.options.resume_type = self.options.resume_type.strip("\"")


        if (self.options.page_delay < 0):
            self.options.page_delay = 0        

        if (self.options.mode == "model"):
            return
        if (self.options.mode == "options"):
            return
        if (self.options.mode == "timing"):
            return
        if (self.options.mode == "csv"):
            skipSerial = True
        if (self.options.mode == "text"):
            return                        
        if (self.options.mode == "version"):    
#             inkex.errormsg( gettext.gettext(self.versionString)) # Accessible from CLI only
            return            

        import axidraw    # https://github.com/evil-mad/axidraw
        import hershey_advanced

        ad = axidraw.AxiDraw()
        hta = hershey_advanced.HersheyAdv()
                        
        ad.getoptions([])
        self.svg = self.document.getroot()        
        ad.ReadWCBdata( self.svg )
        self.svg_row_old = ad.svg_row_old    # Access params from ReadWCBdata
        ad.called_externally = True

        if skipSerial == False:
            self.serial_port = ebb_serial.openPort()
            if self.serial_port is None:
                inkex.errormsg( gettext.gettext( "Failed to connect to AxiDraw. :(" ))
                return

        if self.options.mode == "autoPlot": 
        
            # Note: In preview mode, we only preview-plot the _last_ row to be plotted.

            pen_down_travel_inches = 0.0 # Local variable
            pen_up_travel_inches =   0.0   # Local variable
            pt_estimate = 0.0 # Local variable
            continue_plotting = True
            
            self.row_to_plot = int(self.options.first_row)

            if (self.options.last_row == 0): # "Continue until last row of data"
                self.options.last_row = 10000  # A large number; only limit by size of data.

            self.ReadCSV()
            if (self.csv_row_count is not None):
    
                if (self.row_to_plot > self.csv_row_count):
                    inkex.errormsg( gettext.gettext( "No merge data found in specified range of rows." ))
                    continue_plotting = False
                
                if ( self.options.last_row < self.options.first_row ):
                    continue_plotting = False
                    inkex.errormsg( 'Nothing to plot; No data rows selected.')    
    
                if (continue_plotting):
                    ad.backup_original = copy.deepcopy(self.original_document)
    
                    while (continue_plotting):
                        self.svg_rand_seed =  round(time.time() * 100)/100    # New random seed for new plot
                        self.mergeAndPlot(hta, ad)
                        
                        if self.spewDebugdata:
                            inkex.errormsg( 'Merging row number ' + str(int(self.row_to_plot))  + '.')    
    
                        pen_down_travel_inches = pen_down_travel_inches + ad.pen_down_travel_inches # Local copy
                        pen_up_travel_inches =   pen_up_travel_inches   + ad.pen_up_travel_inches   # Local copy
                        pt_estimate = pt_estimate + ad.pt_estimate # Local copy
    
                        if (ad.b_stopped): # A pause was triggered while plotting the previous row.
                            inkex.errormsg( 'Paused while plotting row number ' + str(int(self.row_to_plot))  + '.')
                            continue_plotting = False                    
                        else:    # Finished plotting the row without being paused
        
                            self.row_to_plot = self.row_to_plot + 1
        
                            if (self.row_to_plot > self.options.last_row):
                                continue_plotting = False # We have already finished the last row.
                            else:    # We will be plotting at least one more row. Delay first.
                                self.next_csv_row() 
                                self.delay_between_rows = True        # Indicate that we are currently delaying between copies
                                timeCounter = 10 * self.options.page_delay  # 100 ms units
                                if self.spewDebugdata:
                                    inkex.errormsg( 'Delaying ' + str(int(self.options.page_delay))  + ' seconds.')    
                                while (timeCounter > 0):    
                                    timeCounter = timeCounter - 1
                                    if (self.b_stopped == False):
                                        if self.options.preview:
                                            pt_estimate += 100    
                                            self.pageDelays += 0.1
                                        else:
                                            time.sleep(0.100)            # Use short intervals to improve responsiveness
                                            self.PauseCheck()    #Query if button pressed
                                self.delay_between_rows = False        # Not currently delaying between copies
                                if (self.b_stopped == True): # if button pressed
                                    self.row_to_plot = self.row_to_plot - 1 # Backtrack; we didn't actually get to that row.
                                    inkex.errormsg( 'Sequence halted after row number ' + str(int(self.row_to_plot))  + '.')    
                                    continue_plotting = False # Cancel plotting sequence
        
                    ad.pen_down_travel_inches = pen_down_travel_inches # Copy local values back to ad.(values)
                    ad.pen_up_travel_inches =   pen_up_travel_inches   #  for printing time report.
                    ad.pt_estimate = pt_estimate 
                    self.printTimeReport(ad)
            

        elif self.options.mode == "singlePlot": 
        
            doPlot = True
            
            if ( self.options.single_type == "singleFix" ): # Plot a specified row
                self.row_to_plot = int(self.options.single_row)
            elif ( self.options.single_type == "singleAdv" ): # Automatically advance
                self.row_to_plot = int(self.svg_row_old + 1)
            else: # ( self.options.single_type == "queryRow" )
                # No plotting; Query and report last row plotted
                inkex.errormsg( 'Last row merged: Row number ' + str(int(self.svg_row_old)) )    
                inkex.errormsg( 'Next row to merge: Row number ' + str(int(self.svg_row_old + 1)) )    
                doPlot = False
            
            if doPlot:
                self.svg_rand_seed =  round(time.time() * 100)/100    # New random seed for new plot
                self.options.last_row = self.row_to_plot # Last row is equal to first row, in this case.
                self.ReadCSV()
                if (self.csv_row_count is not None):
                    
                    if (self.row_to_plot > self.csv_row_count):
                        inkex.errormsg( gettext.gettext( "No merge data found in row number " ) + str(self.row_to_plot) + '.')
                    else:
                        ad.backup_original = copy.deepcopy(self.original_document)
                        self.mergeAndPlot(hta, ad)
                        self.printTimeReport(ad)

        elif self.options.mode == "resume":
        
            ad.options.mode = "resume" 
            self.svg_rand_seed = ad.svg_rand_seed_old     # Preserve random seed
            self.row_to_plot = self.svg_row_old         # Preserve SVG Row
            ad.options.resume_type = self.options.resume_type

            if ( self.options.resume_type == "home" ):
                self.options.fontface = "none"    # Disable Hershey Text substitution
                self.mergeAndPlot(hta, ad)
            elif (ad.svg_application_old != "Axidraw Merge"):
                inkex.errormsg( gettext.gettext( "No AxiDraw Merge resume data found in file." ))
            elif ( ad.svg_layer_old == 12345 ):  # There appears to be a paused "all layers" plot
                self.options.last_row = self.row_to_plot
                self.ReadCSV()
                
                if (self.csv_row_count is not None):
    
                    ad.backup_original = copy.deepcopy(self.original_document)
                    self.mergeAndPlot(hta, ad)
                    self.printTimeReport(ad)
            else:
                inkex.errormsg( gettext.gettext( "No in-progress plot data found saved in file." ))

        elif self.options.mode == "setup":
        
            if self.options.preview:
                inkex.errormsg( gettext.gettext('Command unavailable while in preview mode.'))
            else:
                    
                ad.options.mode = self.options.mode
                ad.options.setup_type = self.options.setup_type
                
                ad.options.pen_pos_up = self.options.pen_pos_up
                ad.options.pen_pos_down = self.options.pen_pos_down
                ad.document = self.document
                ad.options.port = self.serial_port
                ad.effect()

        elif self.options.mode == "csv":
            #  Open file dialog

            if self.options.data_action == "choose": 
                # Select and upload a CSV file
                
                try:
                    import pygtk
                    pygtk.require('2.0')
                    import gtk    # Use gtk to create file selection dialog box.
                    # self.useGTK = True
                except:
                    inkex.errormsg( "Unable to load GTK, a required component. Please contact technical support for assistance.")
                    return
            
                filename = None
    
                dialog = gtk.FileChooserDialog(title="Please choose a CSV file",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
    
                dialog.set_default_response(gtk.RESPONSE_OK)
                
                filter = gtk.FileFilter()
                filter.set_name("Text/CSV")
                filter.add_pattern("*.CSV")
                filter.add_pattern("*.csv")
                filter.add_pattern("*.txt")
                filter.add_pattern("*.TXT")
                filter.add_mime_type("text/csv")
                filter.add_mime_type("text/plain")
                filter.add_mime_type("application/csv")
                filter.add_mime_type("application/x-csv")
                filter.add_mime_type("text/x-csv")
                filter.add_mime_type("text/csv")
                filter.add_mime_type("text/comma-separated-values")
                filter.add_mime_type("text/x-comma-separated-values")
                filter.add_mime_type("text/tab-separated-values")
                dialog.add_filter(filter)
                filter = gtk.FileFilter()
                filter.set_name("All files")
                filter.add_pattern("*")
                dialog.add_filter(filter)
    
                response = dialog.run()
        
                if response == gtk.RESPONSE_OK:
                    filename = dialog.get_filename()
                    #inkex.errormsg( "File selected: " + filename) # Print full path
                    # inkex.errormsg( "Selected file: " + str(os.path.basename(filename))) # Print file name
                elif response == gtk.RESPONSE_CANCEL:
                    inkex.errormsg( gettext.gettext('No CSV file selected.'))
                filter.destroy()
                dialog.destroy()
    
                if filename is not None:
        
                    CSVfile = open(filename, 'rU')
                    try:
                        dialect_read = csv.Sniffer().sniff(CSVfile.readline())
                    except:
                        dialect_read = None
                        inkex.errormsg( "Unable to determine format of selected file, " \
                                + str(os.path.basename(filename)) ) # Print file name
                    
                    if dialect_read is None:
                        CSVfile.close()
                    else:
                        CSVfile.seek(0)    # Rewind file to beginning
            
                        reader = csv.reader(CSVfile,dialect=dialect_read)
                        CSVrowCount = sum(1 for row in reader) - 1 # Subtract 1 for header row
                        CSVfile.seek(0)
    
                        if (CSVrowCount > 0):
                            CSVfile = open(filename, 'rU')
                            reader = csv.DictReader(CSVfile,dialect=dialect_read)
        
                            inkex.errormsg( "Found " + str(CSVrowCount) + " Rows of merge data in file " \
                                        + str(os.path.basename(filename))) # Print file name
                            key_names = "Column names: " 
                            for item in reader.fieldnames:
                                key_names = key_names + "{{" + item + "}}, " 
                            key_names = key_names[:-2]  # drop last two characters from string (", ")
                            inkex.errormsg( key_names ) # Print key list

                            self.csv_file_path = str(filename)    # Path & Name of the file
                            self.storeCSVpath(self.svg)        # Store path & name file in our SVG file.
                        else:
                            inkex.errormsg( "Unable to interpret selected file" + str(os.path.basename(filename)) + ".") 
                        CSVfile.close()

            elif self.options.data_action == "view":
                self.csv_data_read = False
                CSVfile = None
                csvNode = None
                for node in self.svg:
                    if node.tag == 'svg':
                        for subNode in self.svg:
                            if subNode.tag == inkex.addNS( 'MergeData', 'svg' ) or subNode.tag == 'MergeData':
                                csvNode = subNode
                    elif node.tag == inkex.addNS( 'MergeData', 'svg' ) or node.tag == 'MergeData':
                        csvNode = node
                if csvNode is not None:
                    try:
                        CSVfile = str( csvNode.text ) 
                        self.csv_data_read = True
                    except:
                        self.svg.remove( csvNode ) # An error before this point leaves csvDataRead as False. 
        
                if CSVfile is None:
                    inkex.errormsg( "No CSV data found in file. Please select and load a CSV file." )
                    return
                else:
                    inkex.errormsg( "The selected CSV data file is:" )
                    inkex.errormsg(CSVfile)
                
#             elif self.options.data_action == "erase":
#                 self.eraseCSVpath(self.svg)    # erase stored CSV file from our SVG file.

        if self.serial_port is not None:
            ebb_motion.doTimedPause(self.serial_port, 10) #Pause a moment for underway commands to finish...
            ebb_serial.closePort(self.serial_port)    

    def ReadCSV( self ):
        '''
        *    Before looking at the SVG document, parse the CSV data. 
        *    Count the rows
        *    Initialize a dictionary with column header names as keys
            and values from the first row to be merged.
        '''

        # Read CSV Merge data, stored as CDATA in a custom "MergeData" XML element
        self.csv_data_read = False
        CSVfile = None
        csvNode = None
        fileName = None

        for node in self.svg:
            if node.tag == 'svg':
                for subNode in self.svg:
                    if subNode.tag == inkex.addNS( 'MergeData', 'svg' ) or subNode.tag == 'MergeData':
                        fileName = str(subNode.text)
            elif node.tag == inkex.addNS( 'MergeData', 'svg' ) or node.tag == 'MergeData':
                fileName = str(node.text)


        if fileName is None:
            inkex.errormsg( "No CSV file name selected. Use Data tab to select a CSV file." )
            return
        else:
            # inkex.errormsg( "File: " + str(filename))
            try:
                CSVfile = open(fileName, 'rU')
            except:
                inkex.errormsg( "CSV data file not found. Use Data tab to select a CSV file." )

            if CSVfile is not None:
                try:
                    CSVfile = CSVfile.read()
                except:
                    inkex.errormsg( "No CSV data found in file. Use Data tab to select a CSV file." )
            
        if CSVfile is None:
            return

        CSVfile  = '\n'.join(CSVfile.splitlines())

        dialect_read = csv.Sniffer().sniff(StringIO(CSVfile).readline())
#         self.reader = csv.reader(StringIO(CSVfile),dialect=dialect_read)


#         inkex.errormsg( "Dialect doublequote: " + str(dialect_read.doublequote)  )  # Debug use only.
#         inkex.errormsg( "Dialect delimiter:" + str(dialect_read.delimiter)  )  # Debug use only.
#         inkex.errormsg( "Dialect quotechar:" + str(dialect_read.quotechar)  )  # Debug use only.
#         inkex.errormsg( "Dialect quoting:" + str(dialect_read.quoting)  )  # Debug use only.
#         inkex.errormsg( "Dialect escapechar:" + str(dialect_read.escapechar)  )  # Debug use only.
#         dialect_read.escapechar = 

        dialect_read.doublequote = True # Force two quotes ("") to be read as an escaped quotation mark.
        # This is a hack for excel compatibility; it may cause issues with some less common encodings.
        
        self.reader = csv.reader(StringIO(CSVfile),dialect_read)


        self.csv_row_count = sum(1 for row in self.reader) - 1 # Subtract 1 for header row
        
        # This count exhausts the reader by iteration; we need to reset the reader:
        self.reader = csv.DictReader(StringIO(CSVfile),dialect=dialect_read)

        if (self.csv_row_count < self.options.last_row):
            self.options.last_row = self.csv_row_count # Limit last row of data to end of CSV file

#         inkex.errormsg( 'row count: ' + str(self.csv_row_count) )        # Report number of rows. Debug use only.
#         inkex.errormsg( 'fieldnames: ' + str(self.reader.fieldnames) ) # List field names. Debug use only.
#         inkex.errormsg( 'self.row_to_plot: ' + str(self.row_to_plot) )
#         inkex.errormsg( 'self.options.last_row: ' + str( self.options.last_row) )

        if (self.row_to_plot > self.csv_row_count):
            return

        # Initialize dictionary for _first row_ that we'll be merging.
        # This may not be the first data row in the file, depending on which the user has selected.
    
        currentRow = 1
        row = next(self.reader)
        if (self.row_to_plot <= self.options.last_row): # If we are merging any rows,
            while (currentRow < self.row_to_plot):  # If we are not at the first row to merge
                row = next(self.reader)
                currentRow += 1

        self.rowDictionary = {}    # Initialize the row dictionary
        for item in self.reader.fieldnames:
            self.rowDictionary['{{' + item + '}}'] = row[item]
            
#         # Print results
#         inkex.errormsg( 'rowDictionary follows: ')
#         for item in self.rowDictionary:
#             inkex.errormsg( item + ': ' + str(self.rowDictionary[item]) )


    def next_csv_row( self ):
        # Advance to next row of CSV file, and update dictionary
        # with values from the next row.
        row = next(self.reader)
        for item in self.reader.fieldnames:
            self.rowDictionary['{{' + item + '}}'] = row[item]


        
    def mergeAndPlot( self, htRef, adRef ):
        # Merge and plot the actual SVG document, if so selected in the interface
        # Note that merging is a separate operation, that _does not require_ that
        # Hershey Advanced is used. Merged data may take many forms, including
        # purely graphical, e.g., a saved signature


        '''
        Order of operations:
        0. Make a backup copy of the document
        1. Merge the correct row of text data, if selected
        2. Perform Hershey text substitution, if selected, using Hershey Advanced
            * If plotting a new document, use new random seed
            * If resuming, use random seed from document.
        3. Plot the document, using axidraw.py
            * We do not actually need to send the random seed to axidraw.py.
            * axidraw.py will replace SVG data with _original_ (backup) SVG data
              before appending preview and progress data.
        4. Collect WCB data output from axidraw.py and modify
            * Save merge row number (perhaps in place of layer)
            * Save random seed that we used for Hershey text, overruling that in the WCB data.    
            

        Strategy:

        * For each row to be merged:
            * Update dictionary  
            * Use regular expressions  _once_ to replace text via dictionary
                *    Start with string version of etree
                *    https://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
                *    Convert back to etree
        
        '''

        
        if ((self.options.mode == "resume") and ( self.options.resume_type == "home" )):
            pass    # perform no merging
        else:        # perform merge operation
            xmlstr = etree.tostring(self.document, encoding='utf8', method='xml')
            # inkex.errormsg( 'xmlstr: ' + xmlstr)    # Print etree as string (debug only)
            regex = compile("(%s)" % "|".join(map(escape, self.rowDictionary.keys())))
            result = regex.sub(lambda mo: self.rowDictionary[mo.string[mo.start():mo.end()]], xmlstr)
            # inkex.errormsg( 'xmlstr: ' + xmlstr)    # Print etree as string (debug only)
            p = etree.XMLParser(huge_tree=True)
            self.document = etree.parse(StringIO(result), parser=p)

        # 2. Perform Hershey text substitution, if selected, using Hershey Advanced
        if ( self.options.fontface != "none" ):
            htRef.getoptions([])
            htRef.options.fontface         = self.options.fontface
            htRef.options.enable_defects = self.options.enable_defects
            htRef.options.baseline_var     = self.options.baseline_var
            htRef.options.indent_var     = self.options.indent_var
            htRef.options.kern_var         = self.options.kern_var
            htRef.options.size_var         = self.options.size_var
            htRef.options.letter_spacing = self.options.letter_spacing
            htRef.options.word_spacing     = self.options.word_spacing
            htRef.options.rand_seed        = self.svg_rand_seed 
            htRef.options.preserve_text    = False
            htRef.document                 = self.document
            htRef.effect()
            
        # 3. Plot the document, using axidraw.py

        # Many plotting parameters to pass through:
        #adRef.options.mode             = "plot"  # Default value; should not need to actively set
        adRef.options.pen_pos_up     = self.options.pen_pos_up
        adRef.options.pen_pos_down = self.options.pen_pos_down

        adRef.options.speed_pendown     = self.options.speed_pendown
        adRef.options.speed_penup         = self.options.speed_penup
        adRef.options.accel         = self.options.accel
        
        adRef.options.pen_rate_raise     = self.options.pen_rate_raise
        adRef.options.pen_rate_lower     = self.options.pen_rate_lower
        adRef.options.pen_delay_up     = self.options.pen_delay_up
        adRef.options.pen_delay_down     = self.options.pen_delay_down

        adRef.options.auto_rotate         = self.options.auto_rotate
        adRef.options.const_speed         = self.options.const_speed
        adRef.options.report_time         = self.options.report_time

        adRef.options.resolution         = self.options.resolution
        adRef.options.smoothness         = axidraw_merge_conf.smoothness
        adRef.options.cornering         = axidraw_merge_conf.cornering
        adRef.options.preview         = self.options.preview
        adRef.options.rendering         = self.options.rendering
        adRef.options.model             = self.options.model
        adRef.options.copies     = 1

        if not self.options.preview:
            adRef.options.port             = self.serial_port

        # Pass the document off for plotting
        adRef.document = self.document 
        
        # Plot the document using axidraw.py
        adRef.effect()    
        self.rows_plotted += 1

        # 4. Collect WCB data output from axidraw.py and modify

        # Retrieve the modified version of the document, which may contain 
        # updated data, such as the preview and/or save data
        self.document = adRef.document 
        self.svg  = self.document.getroot()
        
        # Save merge row number (perhaps in place of layer)
        # Save random seed that we used for Hershey text, overruling that in the WCB data.    
        
        self.svg_data_written = False    
        self.modifySVGWCBData( self.svg )


    def PauseCheck (self):
        # Check to see if pause button was pressed while delaying between copies.
                
        if self.b_stopped:
            return    # We have _already_ halted the plot due to a button press. No need to proceed.
            
        if self.options.preview:
            strButton = ['0']
        else:
            strButton = ebb_motion.QueryPRGButton(self.serial_port)    #Query if button pressed
        try:
            pauseState = strButton[0]
        except:
            inkex.errormsg( '\nUSB Connectivity lost.') 
            pauseState = '2' # Pause the plot; we appear to have lost connectivity.
            if self.spewDebugdata:
                inkex.errormsg( '\n USB Connectivity lost' )    

        if ((pauseState == '1') and (self.delay_between_rows == False)):
            if self.spewDebugdata:
                inkex.errormsg( '\n Paused by button press. ' )    

        if (pauseState == '1') or (pauseState == '2'):  # Stop plot
            if (self.delay_between_rows == False):    # Only say this if we're not in the delay between copies.
                inkex.errormsg( 'Use the "resume" feature to continue.' )
            self.b_stopped = True

    def modifySVGWCBData( self, aNodeList ):
        # Set/override parameters saved in the SVG.
        # Specifically, update parameters specific to merging.
        if ( not self.svg_data_written ): # Ensure that we only run this once
                for node in aNodeList:
                    if node.tag == 'svg':
                        self.modifySVGWCBData( node )
                    elif node.tag == inkex.addNS( 'WCB', 'svg' ) or node.tag == 'WCB':
                        node.set( 'application', "Axidraw Merge" )            # Name of this program
                        node.set( 'row', str( self.row_to_plot ) )            # Data merge row number
                        node.set( 'randseed', str( (self.svg_rand_seed) ) )    # Random seed for this row
                        self.svg_data_written = True

    def storeCSVpath( self, aNodeList ):
        if ( not self.csv_data_written ): # First, check for existing MergeData node:
            for node in aNodeList:
                if node.tag == 'svg':
                    self.storeCSVpath( node )
                elif node.tag == inkex.addNS( 'MergeData', 'svg' ) or node.tag == 'MergeData':
                    node.text = etree.CDATA(self.csv_file_path)
                    self.csv_data_written = True
        if ( not self.csv_data_written ): # Else, add the element, then try again.
            etree.SubElement( self.svg, 'MergeData' )
            self.storeCSVpath( aNodeList )

#     def eraseCSVpath( self, aNodeList ):
#         self.csvDataErased = False
#         if ( not self.csvDataErased ): # First, check to see if we have already finished:
#             for node in aNodeList:
#                 if node.tag == 'svg':
#                     self.eraseCSVpath( node ) # Recursively call if necessary
#                 elif node.tag == inkex.addNS( 'MergeData', 'svg' ) or node.tag == 'MergeData':
#                     aNodeList.remove( node )
#                     self.csvDataErased = True

    def printTimeReport( self, adRef ):
        if (self.options.report_time):
            if self.options.preview:
                m, s = divmod(adRef.pt_estimate/1000.0, 60)
                h, m = divmod(m, 60)
                if (h > 0):
                    inkex.errormsg("Estimated print time: %d:%02d:%02d (Hours, minutes, seconds)" % (h, m, s))
                else:
                    inkex.errormsg("Estimated print time: %02d:%02d (minutes, seconds)" % (m, s))
                if (self.pageDelays > 0):
                    inkex.errormsg(" including %d s of delays between pages." % (round(self.pageDelays)))

            elapsed_time = time.time() - self.start_time
            m, s = divmod(elapsed_time, 60)
            h, m = divmod(m, 60)
            downDist = 0.0254 * adRef.pen_down_travel_inches
            totDist = downDist + (0.0254 * adRef.pen_up_travel_inches)
            if self.options.preview:
                inkex.errormsg("Total rows to merge and plot: %d." % self.rows_plotted)
                inkex.errormsg("Length of path to draw: %1.2f m." % downDist)
                inkex.errormsg("Total movement distance: %1.2f m." % totDist)
                inkex.errormsg("This estimate took: %d:%02d:%02d (Hours, minutes, seconds)" % (h, m, s))
            else:
                if (h > 0):
                    inkex.errormsg("Elapsed time: %d:%02d:%02d (Hours, minutes, seconds)" % (h, m, s))
                else:
                    inkex.errormsg("Elapsed time: %02d:%02d (minutes, seconds)" % (m, s))
                if (self.rows_plotted > 1):
                    inkex.errormsg("Total rows plotted: %d." % self.rows_plotted)
                inkex.errormsg("Length of path drawn: %1.2f m." % downDist)
                inkex.errormsg("Total distance moved: %1.2f m." % totDist)


if __name__ == '__main__':
    e = AxiDrawMergeClass()
    e.affect()
