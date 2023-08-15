from user import account
from tickers import tickers

import pandas as pd
import requests

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

class algorithm():

    def __init__(self):
        
        self.account = account()
        self.trading_client = self.account.getAccount()
        self.keys = self.account.getKeys()

        self.ticker = tickers()
        self.stock_df = self.ticker.getStock()

        # HTTP request header
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": self.keys[1],
            "APCA-API-SECRET-KEY": self.keys[2]
        }

        self.endpoint_positions = self.keys[0] + "/v2/positions"
        self.endpoint_orders = self.keys[0] + "/v2/orders"

    # Init start of day values
    def openDay(self):
        self.ticker.dailyOpen()

    # Called periodically to make a decision whether to place order
    def checkState(self):
        self.ticker.updateValues()

        for x in self.stock_df.index:
            ticker1 = self.stock_df["class_A"]
            ticker2 = self.stock_df["class_B"]
            ticker1_price = self.stock_df["current_price_A"]
            ticker2_price = self.stock_df["current_price_B"]

            margin_open = self.stock_df["open_price_margin"]
            margin_current = self.stock_df["current_price_margin"]
            time_A = self.stock_df["update_time_A"]
            time_B = self.stock_df["update_time_B"]

            # proceed only if both quotes are <= 10 min apart
            if (abs(time_A - time_B) <= 10):

                # Check for buy only if no open positions
                if(self.stock_df["position"][x] == False):

                    # place order
                    if (margin_current >= margin_open * 2):
                        if ticker1_price < ticker2:
                            self.placeOrder(ticker1, ticker2)
                        else:
                            self.placeOrder(ticker2, ticker1)
                        self.stock_df["position"][x] = True
                
                # Check for sell only if open position exists
                if(self.stock_df["position"][x] == True):

                    # sell order
                    if (margin_current <= margin_open * 1.5):
                        # If position is open, sell, else cancel order
                        if self.checkOrder(ticker1, ticker2) == True:
                            self.sellOrder(ticker1, ticker2)
                        else:
                            self.cancelOrder(ticker1, ticker2)
                        self.stock_df["position"][x] = False
            

    # place long on ticker1, place short on ticker2
    def placeOrder(self, ticker1, ticker2):
        # preparing market order
        market_order_data_long = MarketOrderRequest(
                            symbol= ticker1,
                            qty=0.023,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY,
                            client_order_id= ticker1 + "/shivamkak"

                            )

        # Market order
        market_order_long = self.trading_client.submit_order(
                        order_data=market_order_data_long
                    )
        

        # preparing orders
        market_order_data_short = MarketOrderRequest(
                            symbol="SPY",
                            qty=1,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC,
                            client_order_id= ticker1 + "/shivamkak"

                            )

        # Market order
        market_order_short = self.trading_client.submit_order(
                        order_data=market_order_data_short
                    )

    def checkOrder(self, ticker1, ticker2):

        url_ticker1 = self.endpoint_positions + "/" + ticker1
        url_ticker2 = self.endpoint_positions + "/" + ticker2

        response1 = requests.get(url_ticker1, headers=self.headers).json()
        response2 = requests.get(url_ticker2, headers=self.headers).json()

        # Return false if BOTH of the ticker orders has not been processed
        # Avoid edge case where 1 processed and cancelled while other was ordered alone
        if response1["code"] == 40410000 and response2["code"] == 40410000:
             return False
        else:
             return True

    
    # sell long on ticker1, sell short on ticker2
    # HTTP delete request
    def sellOrder(self, ticker1, ticker2):
        url_ticker1 = self.endpoint_positions + "/" + ticker1
        url_ticker2 = self.endpoint_positions + "/" + ticker2

        response_ticker1 = requests.delete(url_ticker1, headers=self.headers)
        response_ticker2 = requests.delete(url_ticker2, headers=self.headers)


    def cancelOrder(self, ticker1, ticker2):
        url_ticker1 = self.endpoint_orders + "/" + ticker1 + "/shivamkak"
        url_ticker2 = self.endpoint_orders + "/" + ticker2 + "/shivamkak"

        response = requests.delete(url_ticker1, headers=self.headers)
        response = requests.delete(url_ticker2, headers=self.headers)


    # Sell any open positions, to be called 1 min before closing
    # HTTP delete request
    def endDay(self):

        response = requests.delete(self.endpoint_positions, headers=self.headers)

        # Check All open positions to confirm empty list:
        open = requests.get(self.endpoint_positions, headers=self.headers)


test = algorithm()
test.endDay()

