## Description
This small utility provides a way to download historical data for multiple tickers from Interactive Brokers via IBAPI. When run, it will collect bar data (e.g., Open, High, Low, Close, Volume) for the specified tickers and write them to CSV files.
## How It Works
1. Connects to an Interactive Brokers TWS or Gateway instance using client parameters defined in the code (e.g., `app.connect("127.0.0.1", 7496, clientId=1)`).
2. Defines a contract for each ticker using a helper function (e.g., setting the symbol, security type, currency, and exchange).
3. Requests historical market data from IB for a specified duration and candle size.
4. Logs the bar data to the console.
5. Writes the retrieved data to CSV files in a “historical_data” directory.

## How to Use
1. Make sure your Interactive Brokers TWS or IB Gateway is running, and note the IP and port it is listening on.
2. In the code, adjust the following as needed:
    - Connection details (e.g., IP address and port):
Replace `"127.0.0.1"` and `7496` with the actual IP and port your TWS or Gateway is using.
    - Client ID:
The default client ID is set to `1`, but you can change it if you need multiple connections.
    - Tickers array:
Modify the array (e.g., `["FB","AMZN"]`) to include the symbols you'd like to download historical data for.
    - Security configuration:
For each ticker, specify the security type, currency, and exchange if needed. The default is `"STK", "USD", "ISLAND"`.
    - Duration and bar size in the function call (e.g., `'5 Y', '1 hour'`):
Change these to your preferred time horizon and bar size.

3. Run the Python file (e.g., via `python ib_hist_multi_ticker.py` in a terminal or command prompt).
4. After the data is retrieved, CSV files will be saved in a generated folder named **historical_data**.

## Required Changes
- If you need different bar size intervals or durations, you can modify the parameters in the function that requests historical data.
- If your TWS or IB Gateway runs on a different port (e.g., 7497 for a paper account), make sure to replace `7496` wherever necessary.
- Other parameters such as `whatToShow`, `formatDate`, and `useRTH` can be customized in the request function to meet your specific data requirements.

## Notes
- Ensure that your IB TWS API settings are properly configured (e.g., “Enable ActiveX and Socket Clients” in TWS).
- This script assumes Python 3.x compatibility and relies on threads to manage asynchronous data retrieval.
- If you observe a timeout message and no data is retrieved, make sure your connection details are correct, your TWS or Gateway is up, and the symbols are valid for retrieval.

## Contribute
If you’d like to contribute or have any questions, feel free to open an issue or submit a pull request once the project is public. Suggestions for improvements or feature requests are welcome!
–––
© 2025, Gui Reis. All rights reserved.

