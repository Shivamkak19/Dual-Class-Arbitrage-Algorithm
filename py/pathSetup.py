from tickers import tickers
import pandas as pd

import requests

r = requests.get('https://api.darqube.com/data-api/market_data/quote/GOOG?token=257ae70a8408461284a148458eb2717f')
print(r.json())

api_auth = "257ae70a8408461284a148458eb2717f"
ticker = tickers()
stock_df = ticker.getStock()

classA_list = []

for i in stock_df.class_A:
    path = "https://api.darqube.com/data-api/market_data/quote/"
    path += i
    path += "?token="
    path += api_auth
    classA_list.append(path)

classB_list = []

for i in stock_df.class_B:
    path = "https://api.darqube.com/data-api/market_data/quote/"
    path += i
    path += "?token="
    path += api_auth
    classB_list.append(path)

# Avoid path truncation
pd.options.display.max_colwidth = 300

stock_df.insert(loc = 1,
          column = 'class_A_Path',
          value = classA_list)

stock_df.insert(loc = 3,
          column = 'class_B_Path',
          value = classB_list)

