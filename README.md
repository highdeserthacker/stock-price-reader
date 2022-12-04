# stock-price-reader
Python program to obtain stock/fund prices given a list of tickers. Generates a csv output file that can be imported e.g. into Excel.
I use this to update a personal financials spreadsheet with the latest pricing.
Utilizes the api provided by [Alpha Advantage](https://www.alphavantage.co/documentation/). 

## Built With
Python

## Setup
Obtain a free api key from [Alpha Advantage](https://www.alphavantage.co/documentation/).

## Usage
~~~
python -u stockprices.py  --apikey myapikey --input dir/input-file.csv --output dir/output-file.csv
-u: (optional) run with output unbuffered, so that debug output shows up real-time.
--input: input file. Text file containing the list of ticker symbols. Comma delimited format, 1 row per ticker.
--output: output csv file with results.
--debug 1: (optional) Debug mode is verbose and does not generate the output file.

Example: python -u /programs/python/stockprices.py  --apikey ABCDEFGHIJKLMNOP  --input tickers.csv --output ~/stockprices.csv
~~~

## Example Input File
~~~
Ticker
IWV
MSFT
VTSAX
~~~

## Example Output File
~~~
Ticker,Price
IWV,220.1600
MSFT,259.5800
VTSAX,91.7700
~~~
