#

import yfinance as yf

# Get a stock quote for a specific company (e.g., Infosys)sss
infy_quote = yf.Ticker("INFY.NS")
if infy_quote:
    # Print the last price from the info dictionary
    print(f"Current price for INFY: {infy_quote.info['currentPrice']}")
