# axidraw_merge_conf.py
# Configuration file for AxiDraw Merge
#
# Version 2.2.0, dated 2018-09-30
#
# Copyright 2018 Windell H. Oskay, Evil Mad Scientist Laboratories
#
# https://github.com/evil-mad/AxiDraw
#
# "Change numbers here, not there." :)


'''
Primary user-adjustable control parameters:

We encourage you to freely tune these values as needed to match the
 behavior and performance of your AxiDraw to your application and taste.

If you are operating the AxiDraw from within Inkscape (either within the
 application from the Extensions menu or from the command line), please
 set your preferences within Inkscape, using the AxiDraw Control dialog.
 (The values listed here are ignored when called via Inkscape.)

If you are operating the AxiDraw in "standalone" mode, that is, outside
 of the Inkscape context, then please set your preferences here or via
 command-line arguments. (Preferences set within Inkscape -- via the 
 AxiDraw Control dialog -- are ignored when called via the command line.)
 Recommended practice is to adjust and test settings from within the
 Inkscape GUI, before moving to stand-alone (CLI-based) control.
 
 
'''

# Data merge parameters
firstRow = 1            # Merge Start Row. 
lastRow = 0                # Merge End row. Value of 0: Continue until end of data
page_delay = 10            # Seconds to delay between copies
singleRow = 1            # Specified Row to Merge

# Plotting parameter defaults:

speed_pendown = 25      # Maximum plotting speed, when pen is down (1-100)
speed_penup = 75        # Maximum transit speed, when pen is up (1-100)
accel = 75              # Acceleration rate factor (1-100)

pen_pos_up = 60         # Height of pen when raised (0-100)
pen_pos_down = 30       # Height of pen when lowered (0-100)

pen_rate_raise = 75     # Rate of raising pen (1-100)
pen_rate_lower = 50     # Rate of lowering pen (1-100)

pen_delay_up = 0        # Optional delay after pen is raised (ms)
pen_delay_down = 0      # Optional delay after pen is lowered (ms)

const_speed = False     # Use constant velocity mode when pen is down.
report_time = False     # Report time elapsed.
default_Layer = 1       # Layer(s) selected for layers mode (1-1000).

page_delay = 15         # Optional delay between copies (s).

preview = False         # Preview mode; simulate plotting only.
rendering = 3           # Preview mode rendering option (0-3)
                            # 0: Do not render layers
                            # 1: Render only pen-down movement
                            # 2: Render only pen-up movement
                            # 3: Render all movement

model = 1             # AxiDraw Model (1-3). 1: AxiDraw V2 or V3, default. 2: AxiDraw V3/A3. 3: AxiDraw V3 XLX
port = None           # Serial port or named AxiDraw to use

# Effective motor resolution is approx. 1437 or 2874 steps per inch, in the two modes respectively.
# Note that these resolutions are defined along the native axes of the machine (X+Y) and (X-Y),
# not along the XY axes of the machine. This parameter chooses 8X or 16X microstepping on the motors.


resolution = 1        # Resolution: Either 1 for (smoother, slightly slower) high resolution mode or 2 (coarser) low resolution
auto_rotate = True     # Auto-select portrait vs landscape orientation







# Text substitution parameters

fontface = "EMSBird"  # Default font face (%).

letterSpacing = 100   # Override letter spacing (percent).    Range: 50 - 400 
wordSpacing = 100     # Override word spacing (percent).        Range: 50 - 600 

enableDefects = False # Enable Handwriting Defects. True or False.

baselineVar = 15      # Variation in text baseline, when enableDefects is True (percent). Range: 0 - 100. 
indentVar = 15        # Variation in indent, when enableDefects is True (percent).         Range: 0 - 100.
kernVar = 15          # Variation in kerning, when enableDefects is True (percent).         Range: 0 - 100.
sizeVar = 15          # Variation in font size, when enableDefects is True (percent).     Range: 0 - 100.




'''
Additional user-adjustable control parameters:

These parameters are adjustable only from the command line, and are not
visible from within the Inkscape GUI.

'''

smoothness = 10.0     # Curve smoothing (default: 10.0)

cornering = 10.0      # Cornering speed factor (default: 10.0)


'''
Secondary control parameters:

Values below this point are configured only in this file, not through the user interface(s).
Please note that these values have been carefully chosen, and generally do not need to be 
adjusted in everyday use. That said, proceed with caution, and keep a backup copy.
'''

#Page size values typically do not need to be changed. They primarily affect viewpoint and centering.
#Measured in page pixelssteps.  Default printable area for AxiDraw is 300 x 218 mm

PageWidthIn = 11.81      # Default page width in inches        300 mm = about 11.81 inches
PageHeightIn = 8.58      # Default page height in inches        218 mm = about 8.58 inches


NativeResFactor = 1016.0  # Motor resolution calculation factor, steps per inch, and used in conversions. Default: 1016.0
                          # Note that resolution is defined along native (not X or Y) axes.
                          # Resolution is NativeResFactor * sqrt(2) steps per inch in Low Resolution  (Approx 1437 steps per inch)
                          #       and 2 * NativeResFactor * sqrt(2) steps per inch in High Resolution (Appxox 2874 steps per inch)

MaxStepRate = 24.995      # Maximum allowed motor step rate, in steps per millisecond. 
                          # Note that 25 kHz is the absolute maximum step rate for the EBB.
                          # Movement commands faster than this are ignored; may result in a crash (loss of position control).
                          # We use a conservative value, to help prevent errors due to rounding.
                          # This value is normally used _for speed limit checking only_.

SpeedLimXY_LR = 12.000    # Maximum XY speed allowed when in Low Resolution mode, in inches per second.  Default: 12.000 Max: 17.3958
SpeedLimXY_HR = 8.6979    # Maximum XY speed allowed when in High Resolution mode, in inches per second. Default: 8.6979, Max: 8.6979
                          # Do not increase these values above Max; they are derived from MaxStepRate and the resolution.

MaxStepDist_LR = 0.000696  # Maximum distance covered by 1 step in Low Res mode, rounded up, in inches. ~1/(1016 sqrt(2))
MaxStepDist_HR = 0.000348  # Maximum distance covered by 1 step in Hi Res mode, rounded up, in inches.  ~1/(2032 sqrt(2))
                           # In planning trajectories, we skip movements shorter than these distances, likely to be < 1 step.

const_speedFactor_LR = 0.5  # When in constant-speed mode, multiply the pen-down speed by this factor. Default: 0.5 for Low Res mode
const_speedFactor_HR = 0.4  # When in constant-speed mode, multiply the pen-down speed by this factor. Default: 0.3 for Hi Res mode

StartPosX = 0              # Parking position, in pixels. Default: 0
StartPosY = 0              # Parking position, in pixels. Default: 0

# Acceleration & Deceleration rates:
AccelRate = 40.0           # Standard acceleration rate, inches per second squared    
AccelRatePU = 60.0         # Pen-up acceleration rate, inches per second squared

TimeSlice = 0.025          # Interval, in seconds, of when to update the motors. Default: TimeSlice = 0.025 (25 ms)

#Set a tolerance value, to avoid error messages if a "zero" position rounds to -0.0000010 or something.
BoundsTolerance = 0.001    # Allow movements outside of declared bounds by this distance, in inches.

#Skip pen-up moves shorter than this distance, when possible:
MinGap = 0.010             # Distance Threshold (inches)

# Servo motion limits, in units of (1/12 MHz), about 83 ns:
ServoMax = 27831           # Highest allowed position; "100%" on the scale.    Default value: 25200 units, or 2.31 ms.
ServoMin = 9855            # Lowest allowed position; "0%" on the scale.        Default value: 10800 units, or 0.818 ms.

# Note that previous versions of this configuration file used a wider range, 7500 - 28000, corresponding to a range of 625 us - 2333 us.
# The new limiting values are equivalent to 16%, 86% on that prior scale, giving a little less vertical range, but higher resolution.
# More importantly, it constrains the servo to within the travel ranges that they are typically calibrated, following best practice.

