class Trade:
    def __init__(self,price,volume):
        self.price =price
        self.volume = volume
    def is_buy(self):
        return self.volume > 0
    def __repr__(self):
        return f"Trade({self.price}@ ${self.volume})"

class TradeTracker:
    def __init__(self):
        self.trades = []
    def add_trade(self,trade:Trade):
        self.trades.append(trade)

    def get_buy_trades(self):
         l=[]
         for trade in self.trades:
            if trade.is_buy()==True:
                l.append(trade)
            else:
                print(trade,'is not a buy')
            return l
    def get_average_traded_price(self):
        total = 0
        for trade in self.trades:
            total+=trade.price
        return total/len(self.trades)












































