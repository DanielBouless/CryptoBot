from indicatorwebsocket import myWebsocketClient
from Indicator import Coin
from Indicatorv3 import Price
import time


products = ["BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD"]

ws = myWebsocketClient()
ws.start()

time.sleep(5)
btc = Coin("BTC-USD", 1, 0.01)
eth = Coin("ETH-USD", 1, 0.01)
ada = Coin("ADA-USD", 100, 0.1)
sol = Coin("SOL-USD", 1, 0.01)

while True:

    adapurchase = ada.purchase_price()
    adasell = ada.sell_price()

    print(f"purchase {adapurchase}")
    print(f" sell {adasell}")
    print("\n")
    time.sleep(1)
