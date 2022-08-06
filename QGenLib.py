# QGenLib.py

# ================ Logging ================
import os
import logging

# ================================================================
# Set up logging - Note that it does not print to stdout too.
# Inputs: file name - of the form "/somepath/myapp.py"
#
def LogSetup(LogFileNamePrefix) :
  AppFullFileName= LogFileNamePrefix
  AppNameSplitExt= os.path.splitext(AppFullFileName)  # [0]=path/name, [1]= ext
  LogFileName= AppNameSplitExt[0] + '.log'

  logging.basicConfig(filename=LogFileName,
                      encoding='utf-8',
                      level=logging.INFO,
                      filemode='a',
                      # %(msecs)d - msec as int. %(name)s - username as string. %(levelname)s - debug level as string.
                      format='[%(asctime)s %(levelname)s]: %(message)s',
                      #datefmt='%H:%M:%S'
                      # %a - day of week, %d - day of month, %b - month
                      datefmt='%a, %d %b %Y %H:%M:%S'
                      )


# ================================================================
# Output to tty & log file
# Inputs:
#   LogLevel - Error, Warning, Info
def LogWrite(LogLevel, Message) :
  print(Message)
  # TBD - print at appropropriate level
  # logging.INFO = 20
  logging.info(Message)

def LogWrite(Message) :
  print(Message)
  logging.info(Message)

