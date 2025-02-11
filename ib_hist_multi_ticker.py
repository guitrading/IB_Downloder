"""
IBAPI - Getting historical data (multiple tickers)

@author: labq.io
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import os
import csv

class TradingApp(EWrapper, EClient):
    """
    Handles the interface for trading applications by integrating `EWrapper` and `EClient`.

    This class is used to manage interactions with a trading platform, specifically
    for retrieving and storing historical data, handling asynchronous event-driven
    processes, and managing errors during requests. It ensures data consistency and
    provides mechanisms for signaling when data retrieval is complete.

    :ivar data_received: An event used to signal the completion of data retrieval.
    :type data_received: threading.Event
    :ivar data_store: A dictionary for storing retrieved historical data, organized
        by request id (reqId).
    :type data_store: dict[int, list]

    """
    def __init__(self):
        EClient.__init__(self,self)
        self.data_received = threading.Event()  # Initialize the threading event
        self.data_store = {}  # Dictionary to store retrieved data
        
    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

        # Append bar data to the appropriate ticker's storage
        if reqId not in self.data_store:
            self.data_store[reqId] = []

        self.data_store[reqId].append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])

    def historicalDataEnd(self, reqId, start, end):
        print(f"HistoricalDataEnd. ReqId: {reqId}, Start: {start}, End: {end}")
        self.data_received.set()  # Signal that data is complete

    def error(self, reqId, errorCode, errorString):
        print(f"Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorString}")
        
def websocket_con():
    app.run()
    
app = TradingApp()

# Default ports:
# TWS live session: 7496
# TWS paper session: 7497
# IB Gateway live session: 4001
# IB Gateway paper session: 4002
app.connect("127.0.0.1", 7496, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established

# creating object of the Contract class - will be used as a parameter for other function calls
# edit the sec_type, currency and exchange variables as needed.
def security(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract 

def histData(req_num,contract,duration,candle_size):
    app.reqHistoricalData(reqId=req_num, 
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])	 # EClient function to request contract details
    if not app.data_received.wait(timeout=30):
        print(f"Timeout: No data received for request {req_num}")

# Save data to CSV
def save_to_csv(data, filename):
    header = ["Date", "Open", "High", "Low", "Close", "Volume"]
    os.makedirs("historical_data", exist_ok=True)
    filepath = os.path.join("historical_data", filename)
    
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header
        writer.writerows(data)   # Write the data

# Edit/add/remove tickers as needed.
tickers = ["FB","AMZN"]
for ticker in tickers:
    histData(tickers.index(ticker),security(ticker),'5 Y', '1 hour')
    time.sleep(15)  # some latency added to ensure that the contract details request has been processed

# Save all retrieved data to CSV files
for req_id, data in app.data_store.items():
    save_to_csv(data, f"{tickers[req_id]}_historical_data.csv")

# Disconnect after all requests are done
time.sleep(2)
app.disconnect()
