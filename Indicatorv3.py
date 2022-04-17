import pandas as pd


class Coin:
    def __init__(self, ticker, p_qty, gains):
        self.ticker = ticker
        self.p_qty = p_qty
        self.gainsReq = gains
        self.prices = []
        self.gains = []
        self.losses = []
        self.prev_avg_gain = None
        self.prev_avg_loss = None

    def get_price(self):
        with open(f"{self.ticker}.txt", "r") as prices:
            for l in prices:
                self.prices.append(float(l))
        current_price = self.prices[-1]
        return current_price

    def purchase_price(self):
        current_price = self.get_price()
        purchase_price = (current_price * 1.005) * self.p_qty + (
            current_price * self.p_qty
        ) / self.p_qty
        return purchase_price

    def sell_price(self):
        purchase_price = self.purchase_price()
        sellprice = (self.gainsReq / (2.005 * self.p_qty)) + purchase_price
        return sellprice

    def get_index_price(self, x):
        with open(f"{self.ticker}.txt", "r") as prices:
            for l in prices:
                self.prices.append(float(l))
        price = self.prices[x]
        return price

    def avg_14(self):
        sum = 0
        with open(f"{self.ticker}.txt", "r") as prices:
            for l in prices:
                self.prices.append(float(l))
        for i in self.prices[-15:-1]:
            i = float(i)
            sum = sum + i
        avg = sum / 14
        return avg

    def rsi(self, p):
        with open(f"{self.ticker}.txt", "r") as prices:
            for l in prices:
                self.prices.append(float(l))
        if len(self.prices) >= (p + 1):
            i = 0
            while i <= p - 1:
                diff = self.prices[((-1 * p) - 1) + i] - self.prices[(-1 * p) + i]
                i += 1
                if diff > 0:
                    gain = diff
                    loss = 0
                elif diff < 0:
                    gain = 0
                    loss = abs(diff)
                else:
                    gain = 0
                    loss = 0
                self.gains.append(gain)
                self.losses.append(loss)
            self.avg_gain = sum(self.gains) / len(self.gains)
            self.avg_loss = sum(self.losses) / len(self.losses)
            if i > p:
                self.avg_gain = (self.prev_avg_gain * (p - 1) + gain) / p
                self.avg_loss = (self.prev_avg_loss * (p - 1) + loss) / p
            self.prev_avg_gain = self.avg_gain
            self.prev_avg_loss = self.avg_loss
            rs = round(self.avg_gain / self.avg_loss, 2)
            rsi = round(100 - (100 / (1 + rs)), 2)
            return rsi

    def macd(self, span1, span2, span3):
        dfheaders = {"price": self.prices}
        df = pd.DataFrame(dfheaders)
        ema26 = df["price"].ewm(span=span2, adjust=False, min_periods=span2).mean()
        ema12 = df["price"].ewm(span=span1, adjust=False, min_periods=span1).mean()
        macd = ema26 - ema12
        macd_s = macd.ewm(span=span3, adjust=False, min_periods=span3).mean()
        macd_h = macd - macd_s
        df["macd"] = df.index.map(macd)
        df["macd_h"] = df.index.map(macd_h)
        df["macd_s"] = df.index.map(macd_s)
        showthis = df.iloc[-1, 1]
        return showthis

    def cci(self, span):
        high = []
        low = []
        i = 0
        dfheaders = {"price": self.prices}
        df = pd.DataFrame(dfheaders)
        prices = self.prices[(-1 * (span + 1)) : -1]
        for i in range(span):
            if prices[-1 * (span - i)] > prices[-1 * (span)]:
                low.append()
