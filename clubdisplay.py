#! /usr/bin/env python3
# ClubDisply

# updates
# 2019-12-31 init

#
# imports
#
import datetime as dt
import time
import argparse
import logging
import logging.handlers

#
# parsing
#
parser = argparse.ArgumentParser(description="Club Display Demo")
parser.add_argument("-t",
                    "--test",
                    action="store_true",
                    help="for offline testing")
args = parser.parse_args()

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
else:
    logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

#
# defined functions
#

#
# first run items
#

#
# main loop
#

def main():
    timestamp = dt.datetime.now().time()
    logger.info("nowtime = " + str(timestamp)[:5])

    while True:
        try:
            print("testing")
            time.sleep(60) # wait one minute

            timestamp = dt.datetime.now().time()
            if args.test:
                logger.info("nowtime = " + str(timestamp)[:5])

        except KeyboardInterrupt:
            print("\n\nKeyboard exception.  Exiting.\n")
            logger.info("keyboard exception")
            exit()

        except Exception:
            logger.info("program end: " + str(sys.exc_info()[0]))
            exit()
    return

if __name__ == "__main__":
    main()
    exit()
