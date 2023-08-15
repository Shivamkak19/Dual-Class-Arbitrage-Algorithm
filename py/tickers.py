import pandas as pd
import requests
import datetime

# TODO: implement singleton for tickers() class

# List for each dual-class share
class tickers():

    # Initialize all columns of stock_df dataset
    def __init__(self):

        # Avoid path truncation
        pd.options.display.max_colwidth = 300
        
        self.stock_df = pd.read_csv("../shares.csv")
        self.stock_df.columns = ["class_A", "class_B"]

        column_names = ["API_path_A", "open_price_A", "current_price_A", "update_time_A", "json_A", 
                        "API_path_B", "open_price_B", "current_price_B", "update_time_B", "json_B",
                        "open_price_margin", "current_price_margin"]
        
        # Init columns to null values
        self.stock_df[column_names] = None
        self.stock_df["position"] = False

        self.setAPIPath()
        self.dailyOpen()
        self.updateValues()

    # Set API links upon initialization
    def setAPIPath(self):

        api_auth = "257ae70a8408461284a148458eb2717f"

        classA_list = []

        for i in self.stock_df.class_A:
            path = "https://api.darqube.com/data-api/market_data/quote/"
            path += i
            path += "?token="
            path += api_auth
            classA_list.append(path)

        classB_list = []

        for i in self.stock_df.class_B:
            path = "https://api.darqube.com/data-api/market_data/quote/"
            path += i
            path += "?token="
            path += api_auth
            classB_list.append(path)

        df = pd.DataFrame({"API_path_A": classA_list})
        self.stock_df.update(df)

        df = pd.DataFrame({"API_path_B": classB_list})
        self.stock_df.update(df)
    
    # Set opening values for trading day
    def dailyOpen(self):

        open_A = []
        open_B = []
        open_margin = []

        for link in self.stock_df["API_path_A"]:
            r = requests.get(link).json()
            price_A = r['previous_close']
            open_A.append(price_A)
        
        for link in self.stock_df["API_path_B"]:
            r = requests.get(link).json()
            price_B = r['previous_close']
            open_B.append(price_B)

        for i in range(len(open_A)):
            margin = abs(open_A[i] - open_B[i])
            open_margin.append(margin)

        df = pd.DataFrame({"open_price_A": open_A, 
                           "open_price_B": open_B, 
                           "open_price_margin": open_margin})
        
        self.stock_df.update(df)

    
    # Update values of stock_df periodically
    def updateValues(self):

        jsonList_A = []
        currentPrice_A = []
        updateTime_A = []

        jsonList_B = []
        currentPrice_B = []
        updateTime_B = []

        currentMargin = []


        # Access JSON via HTTP request, convert to Python dictionary
        # Access values via dict
        for link in self.stock_df["API_path_A"]:
            r = requests.get(link).json()
            jsonList_A.append(r)
            
            price_A = r["price"]
            time_A = r["timestamp"]

            # Convert ms to s
            time_A = time_A / 1000 

            date = self.toDateTime(time_A)
            
            updateTime_A.append(date)
            currentPrice_A.append(price_A)

        for link in self.stock_df["API_path_B"]:
            r = requests.get(link).json()
            jsonList_B.append(r)

            price_B = r["price"]
            time_B = r["timestamp"]

            # Convert ms to s
            time_B = time_B / 1000 

            date = self.toDateTime(time_B)
            
            # debugging
            # print(type(date))
            # print(date)

            updateTime_B.append(date)
            currentPrice_B.append(price_B)


        # Set Current Margin values
        for i in range(len(currentPrice_A)):
            margin = abs(currentPrice_A[i] - currentPrice_B[i])
            currentMargin.append(margin)


        # Update all values in stock_df
        df = pd.DataFrame({"json_A": jsonList_A, 
                           "json_B": jsonList_B, 
                           "current_price_A": currentPrice_A,
                           "current_price_B" : currentPrice_B,
                           "update_time_A" : updateTime_A,
                           "update_time_B" : updateTime_B,
                           "current_price_margin": currentMargin})
        
        self.stock_df.update(df)
    
    def toDateTime(self, unixTime):

        # convert from unix time to datetime
        date = datetime.datetime.fromtimestamp(unixTime)

        # Format datetime as a string in the desired format
        date = date.strftime('%m%d%H%M')

        # Convert the formatted string to an integer
        date = int(date)

        return date


    def getStock(self):
        return self.stock_df


# Concatonate

test = tickers()
df = test.getStock()
test.updateValues()
test.dailyOpen()
print(df.head())
test.updateValues()
print("gkuh")
print(df["update_time_B"][0])
print(df["update_time_A"][0])

