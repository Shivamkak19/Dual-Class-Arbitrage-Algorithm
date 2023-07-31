from user import account
from tokens import tokens

from pandas import pd 
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

account = account()
trading_client = account.getAccount()

# Create List of Dual-Class shares
portfolio = []

dc1 = ["GOOGL", "GOOG"]
dc2 = ["FOXA", "FOX"]

portfolio = [dc1,dc2]

print(portfolio)







# search for AAPL
aapl_asset = trading_client.get_asset('GOOGL')

if aapl_asset.tradable:
    print('We can trade AAPL.')

test1 = https://api.darqube.com/data-api/market_data/quote/TSLA?token=257ae70a8408461284a148458eb2717f
