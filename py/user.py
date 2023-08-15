from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

class account():
    
    def __init__(self):
        
        # API Authorization Information
        self.key_live = "AK0ZSFQIKNH51OYVKMB2"
        self.secret_live = "h6IJcWc4cK8aWBaeIAc4budigRtqSMvxOyq2J2mB"
        self.endpoint_live = "https://api.alpaca.markets"
        self.key_paper = "PK1VV2Q66XEYIKECOX7Q"
        self.secret_paper = "G2DThPl44znonvTQ3SpUUugy9ODapUQZ1aj3gVVp"
        self.endpoint_paper = "https://paper-api.alpaca.markets"

        #Toggle Between Live and Paper 
        self.live_status = False

        #Access account with appr. keys/secrets
        if self.live_status:
            self.trading_client = TradingClient(self.key_live, self.secret_live, paper = False)
        else:
            self.trading_client = TradingClient(self.key_paper, self.secret_paper, paper = True)

        # Get our account information.
        self.account = self.trading_client.get_account()

        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Check how much money we can use to open new positions.
        print('${} is available as buying power.'.format(self.account.buying_power))

    def getAccount(self):
        return self.trading_client
    
    def getKeys(self):
        if(self.live_status):
            keys = [self.endpoint_live, self.key_live, self.secret_live]
            return keys
        else:
            keys = [self.endpoint_paper, self.key_paper, self.secret_paper]
            return keys
    


    
