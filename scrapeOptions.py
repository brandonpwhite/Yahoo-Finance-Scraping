#!/usr/bin/env python
 
from bs4 import BeautifulSoup
import pandas as pd
import sys
import dryscrape

symbol = sys.argv[1]

session = dryscrape.Session()
session.set_header("user-agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0")
session.set_attribute('auto_load_images', False)
session.visit("http://finance.yahoo.com/quote/%s/options?p=%s" % (symbol, symbol))
session.wait_for(lambda: session.at_css("tr.data-row0"))

soup = BeautifulSoup(session.body(), "lxml")
calls = soup.find_all("table", attrs={"class": "calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"})
puts = soup.find_all("table", attrs={"class": "puts table-bordered W(100%) Pos(r) list-options"})

def extractData(x):
    arr = []
    for row in x[0].find_all("tr"):
        arr.append([])
        for data in row.find_all("td"):
            value = data.get_text().strip()
            arr[-1].append(value)
    arr = filter(lambda x: len(x) == 10, arr)
    return arr

calls = extractData(calls)
puts = extractData(puts)
 
columns = [ "Strike"
          , "ContractName"
          , "Last"
          , "Bid"
          , "Ask"
          , "Change"
          , "PctChange"
          , "Volume"
          , "OpenInterest"
          , "ImpliedVolatility" ]
 
calls = pd.DataFrame(calls, columns=columns)
puts = pd.DataFrame(puts, columns=columns)

print calls
print puts
