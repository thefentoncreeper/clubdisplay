#! /usr/bin/env python3
# ClubDisply

# updates
# 2019-12-31 init
# 2020-01-03 set to run

#
# imports
#
from datetime import datetime, timedelta
import time
import sys
import argparse
import logging
import logging.handlers
from gpiozero import LED, RGBLED, Button

#
# parsing
#
parser = argparse.ArgumentParser(description="Club Display Demo")
parser.add_argument("-t",
                    "--test",
                    action="store_true",
                    help="no outputs for offline testing")
parser.add_argument(
    "-d",
    "--delay",
    default=0,
    type=int,
    help="delay time in mills")

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="more verbose logging")

args = parser.parse_args()

delay = int(args.delay)


#
# logging
#
# set up a specific logger with desired output level
LOG_FILENAME = "clubdisplay.log"

logger = logging.getLogger("ClubDisplayLogger")

# add the rotating log message handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                          maxBytes=100000,
                                          backupCount=5)
if args.test:
    logger.setLevel(logging.DEBUG)
    fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)


#
# verbose
#
if args.verbose:
    logger.setLevel(logging.DEBUG)
    fh.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)


#
# variables
#
if not args.test:
    signal = LED(4)
    rgb = RGBLED(red=17, green=27, blue=22)
    rgbpower = LED(5)
    button = Button(2)


#
# defined functions
#
def startfunction(stimestamp):
    rgbpower.off()
    signal.off()
    logger.info("Start button pressed")
    logger.info("nowtime = " + format(stimestamp, '%H:%M:%S'))
    sendtime = stimestamp + timedelta(hours=8)
    time.sleep(0.2)
    rgbpower.on()
    signal.on()
    return sendtime


#
# main loop
#

def main():
#
# first run items
#
    timestamp = datetime.now()
    endtime = timestamp
    logger.info("nowtime = " + format(timestamp, '%H:%M:%S'))
    rgbpower.on()
    signal.on()
    stage = 0
    oldstage = -1
    r = 0
    g = 0
    b = 255
    keeprunning = True

    while keeprunning:
        try:
            timestamp = datetime.now()
            if button.is_pressed:
                endtime = startfunction(timestamp)
            else:
                if timestamp > endtime:
                    rgbpower.off()
                    signal.off()

            if stage == 0:
                # blue to violet
                r = r + 1
                if r == 255:
                    stage = stage + 1
            elif stage == 1:
                # violet to red
                b = b - 1
                if b == 0:
                    stage = stage + 1
            elif stage == 2:
                # red to yellow
                g = g + 1
                if g == 255:
                    stage = stage + 1
            elif stage == 3:
                # yellow to green
                r = r - 1
                if r == 0:
                    stage = stage + 1
            elif stage == 4:
                # green to teal
                b = b + 1
                if b == 255:
                    stage = stage + 1
            elif stage == 5:
                # teal to blue
                g = g - 1
                if g == 0:
                    stage = 0

            if stage != oldstage:
                    logger.debug("stage = " + str(stage))
                    logger.debug("nowtime = " + format(timestamp, '%H:%M:%S'))
                    oldstage = stage

            rgb.color = (r/255, g/255, b/255)
            # logger.debug("r ="+str(r)[:3]+", g="+str(g)[:3]+", b="+str(b)[:3])

            time.sleep(delay / 1000)        # wait delay-time

        except KeyboardInterrupt:
            print("\n\nKeyboard exception.  Exiting.\n")
            logger.info("nowtime = " + format(timestamp, '%H:%M:%S'))
            logger.info("keyboard exception")
            rgbpower.off()
            signal.off()
            exit()

        except Exception:
            logger.debug("nowtime = " + format(timestamp, '%H:%M:%S'))
            logger.error("program end: " + str(sys.exc_info()[0]))
            rgbpower.off()
            signal.off()
            exit()

    rgbpower.off()
    signal.off()
    return

if __name__ == "__main__":
    main()
    exit()
