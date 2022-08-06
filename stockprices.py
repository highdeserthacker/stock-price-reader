# stockprices.py - reads a list of tickers and obtains the latest price for each, and placing in the specified output file.
#   Logs to a .log file.
#
#   python -u [ProgramName] --apikey keystr --input /app/my-tickers.csv --output /app/output.csv
#   Parameters:
#     --apikey [key string]   The api key
#     --input  [filename]     The input file containing the ticker symbols.
#     --output [filename]     Output file
#     Optional parameters
#     --debug  1              Debug mode is verbose and does not generate the output file.
#
#   Returns: 0 if ok, !=0 if error
#
#   If running from a python docker container, in the form of e.g.: 
#     docker run --rm -v /dockerdata/programs:/app  python3  python -u /app/stockprices.py  --apikey keystr --input /app/tickers.csv --output /app/stockprices.csv  --debug 1
#     Use -u switch for prints to run unbuffered, so that output shows up real-time.
#
#   Help: [ProgramName] -h
#
#
import sys        # sys.exit()
import time       # time.sleep
import datetime   # localtime
import shutil     # shutil
from pathlib import Path
import csv
import requests   # POST, GET

# ================
# Process command line args. argparse creates an args[] dict for the parameters (sans '--')..
import argparse

parser = argparse.ArgumentParser(description='dripfeed')
parser.add_argument('-k', '--apikey',  help='Api Key', required=True)
parser.add_argument('-i', '--input',  help='Input file', required=True)
parser.add_argument('-o', '--output', help='Output file', required=True)
parser.add_argument('-d', '--debug',  type=int, default=0, help='debug switches. 1= do not generate output file', required=False)
args = vars(parser.parse_args())

ApiKey= args['apikey']
SrcFile= args['input']
DstFile= args['output']
DebugLevel= args['debug']


# ================
# Set up logging - Note that it does not print to stdout too.
from QGenLib import LogSetup, LogWrite
LogSetup(__file__)    # __file__ = e.g. "/app/stockprices.py"

# ================ Main ================

# Process the file. Must contain a header column "Ticker"
Message= "Processing " + SrcFile
LogWrite(Message)
with open(SrcFile, 'r') as csv_file:
  csv_reader= csv.DictReader(csv_file)    # Reads each row as dict
  column_headers= csv_reader.fieldnames   # list of column names

  # Create output file
  OutputHeaderArray= ["Ticker", "Price"]
  OutputRowDict= {
    'Ticker' : 'abc',
    'Price'  : 0
  }

  if DebugLevel == 0 :
    file_writer= open(DstFile, 'w')
    # Write the header
    csv_writer= csv.DictWriter(file_writer, fieldnames=OutputHeaderArray)
    csv_writer.writeheader()


  # Read a row, obtain price for this ticker
  for row in csv_reader :
    Ticker= row['Ticker']
    LogWrite(Ticker)

    # Api call to get the price
    # e.g. https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=ABCDEFGHIJKLMNOP
    # Response is json:
    #{
    #    "Global Quote": {
    #        "01. symbol": "MSFT",
    #        "02. open": "136.9600",
    #        "03. high": "137.5200",
    #        "04. low": "136.4250",
    #        "05. price": "137.3900",
    #        "06. volume": "13611682",
    #        "07. latest trading day": "2019-09-17",
    #        "08. previous close": "136.3300",
    #        "09. change": "1.0600",
    #        "10. change percent": "0.7775%"
    #    }
    #}
    # If error, looks like:
    #{
    #    "Global Quote": {}
    #}
    # Rate limit overage outputs: {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}

    ApiBaseUrl= "https://www.alphavantage.co/query"
    UrlParams= {'function': 'GLOBAL_QUOTE', 'symbol': Ticker, 'apikey': ApiKey}

    r= requests.get(ApiBaseUrl, params=UrlParams)  # Issue the request
    payload_json= r.json()    # get the payload in the form of a dict.
    LogWrite(payload_json)

    # Catch failure to return results
    if 'Global Quote' not in payload_json :
      sys.exit(1)

    Price= payload_json['Global Quote']['05. price']
    Message= "Ticker: " + Ticker + " Price: " + Price
    LogWrite(Message)

    # API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.
    time.sleep(15.000) # seconds to sleep

    # Write to output file
    if DebugLevel == 0 :
      OutputRowDict['Ticker']= Ticker
      OutputRowDict['Price']=  Price
      csv_writer.writerow(OutputRowDict)

# Close output file
if DebugLevel == 0 :
  file_writer.close()


# Exit
sys.exit()    # optional arg (defaults to zero). exit(1) for error


