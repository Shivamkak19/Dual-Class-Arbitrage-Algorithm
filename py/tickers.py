import pandas as pd
import requests

# List for each dual-class share
class tickers():

    # Initialize dual-class shares
    def __init__(self):
        
        self.l2 = ["ARTNA", "ARTNB"]
        self.l3 = ["BELFA", "BELFB"]
        self.l4 = ["BRK.A", "BRK.B"]
        self.l5 = ["BIO", "BIO.B"]
        self.l6 = ["BF.A", "BF.B"]
        self.l7 = ["STZ", "STZ.B"]
        self.l8 = ["FOXA", "FOX"]
        self.l1 = ["GOOGL", "GOOG"]
        self.l9 = ["GEF", "GEF.B"]
        self.l10 = ["LEN", "LEN.B"]

        # parent list for all chares
        self.parent = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9, self.l10]
        self.stock_df = pd.DataFrame(self.parent, columns=["class_A", "class_B"])
        self.setAPIPath()

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

        # Avoid path truncation
        pd.options.display.max_colwidth = 300

        self.stock_df.insert(loc = 1,
                column = 'class_A_API_PATH',
                value = classA_list)

        self.stock_df.insert(loc = 3,
                column = 'class_B_API_PATH',
                value = classB_list)

    def getStock(self):
        return self.stock_df

# Concatonate


ticker = tickers()
df = ticker.getStock()
print(df.head(10))

