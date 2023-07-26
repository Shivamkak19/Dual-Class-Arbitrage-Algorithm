from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

# API Authorization Information
key_live = "AK0ZSFQIKNH51OYVKMB2"
secret_live = "h6IJcWc4cK8aWBaeIAc4budigRtqSMvxOyq2J2mB"
key_paper = "PK1VV2Q66XEYIKECOX7Q"
secret_paper = "G2DThPl44znonvTQ3SpUUugy9ODapUQZ1aj3gVVp"

#Toggle Between Live and Paper 
live_status = True

#Access account with appr. keys/secrets
if live_status:
    trading_client = TradingClient(key_live, secret_live, paper = False)
else:
    trading_client = TradingClient(key_paper, secret_paper, paper = True)

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))