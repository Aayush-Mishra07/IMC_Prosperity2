from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
import math
import pandas as pd

class Trader:
    def __init__(self) -> None:
       self.prices= []
       self.avp1,self.avp2 =[],[]
       self.std_dev=0
       self.def_pos = {'COCONUT_COUPON' : 0, 'COCONUT' : 0, 'AMETHYSTS' : 0,'CHOCOLATE':0,'STRAWBERRIES':0,'ROSES':0,'STARFRUIT':0,'ORCHIDS':0,"GIFT_BASKET":0}
    def moving_av1(self,price):
        self.avp1.append(price)
        if len(self.avp1) > 5:
            self.avp1.pop(0) 
        self.av1 = sum(self.avp1)/len(self.avp1)  
    def moving_av2(self,price):
        self.avp2.append(price)
        if len(self.avp2) > 13:
            self.avp2.pop(0) 
        self.av2 = sum(self.avp2)/len(self.avp2)
    def std(self,price,timestamp):
       self.prices.append(price)
       if len(self.prices) > 5:
            self.prices.pop(0) 
       percent_returns = [(self.prices[i] / self.prices[i-1]) - 1 for i in range(1, len(self.prices))]
       self.std_dev=(np.std(np.array((percent_returns)))*(np.sqrt(99900 - timestamp/99900)))*100
       print(f"stddev:{self.std_dev}")
    def VWAP(self,best_bid,best_bid_amount,best_ask,best_ask_amount):
       self.current_price = (best_bid*best_bid_amount + best_ask*(-best_ask_amount))/(best_bid_amount-best_ask_amount)
       print(f"current price:{self.current_price}")
    def BSM(self,timestamp):
        T=(int((timestamp))/(100*10000))
        d1=np.log(self.current_price/10000)+((((float(self.std_dev))**2)/2)*T)
        self.d1=abs(float(d1)/(float(self.std_dev)*float(np.sqrt(T))))
        self.d2=abs(float(self.d1)-(float(self.std_dev)*float(np.sqrt(T))))
        print(f"d1:{self.d1}")
        print(f"d2:{self.d2}")
    def C(self):
        self.coupon_fair=((self.current_price*(0.5 * (1 + math.erf(self.d1 / math.sqrt(2)))))-(10000*(0.5 * (1 + math.erf(self.d1 / math.sqrt(2))))))
        print(f"coupon_fair:{self.coupon_fair}")

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print(f"market trades: {state.market_trades},own_trades{state.own_trades}")
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))
            if len(order_depth.sell_orders) != 0:
                 best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                 worst_ask,worst_ask_amount = (list(order_depth.sell_orders.items())[::-1])[0]
            if len(order_depth.buy_orders) != 0:
                 best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                 worst_bid, worst_bid_amount = (list(order_depth.buy_orders.items())[::-1])[0]

            if state.market_trades :
              mp =state.market_trades[product][0].price
              mb =state.market_trades[product][0].buyer
              ms =state.market_trades[product][0].seller
              mq =state.market_trades[product][0].quantity
            if state.own_trades:
              op =state.own_trades[product][0].price
              ob =state.own_trades[product][0].buyer
              os = state.own_trades[product][0].seller 
              oq =state.own_trades[product][0].quantity 
            if mb == ms :
                orders.append(Order(product,mp+1,mq)) 

            try:
                    state.position[product]
            except KeyError:
                    state.position[product]=self.def_pos[product]
            if product =="AMETHYSTS":
                    if int(best_ask) < 10000:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 20 - state.position["AMETHYSTS"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if int(best_bid) > 10000:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["AMETHYSTS"] + 20
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol))
            price =(best_ask+best_bid)/2             
            self.moving_av1(price)
            self.moving_av2(price)     
            if product == "COCONUT":
                       
                       self.std(price,state.timestamp)
                       self.VWAP(best_bid,best_bid_amount,best_ask,best_ask_amount)
                       self.BSM(state.timestamp)
                       self.C()
                       
                       if best_ask<self.av1 and (self.av1>self.av2):
                         vol = 300 - state.position["COCONUT"]
                         if vol>0:
                          print("BUY", str(-best_ask_amount) + "x", best_ask)
                          orders.append(Order(product, best_ask, vol))
                          orders.append(Order("COCONUT_COUPON", best_bid, -vol*15))
                       if best_bid>self.av1 and (self.av1<self.av2):
                         vol = state.position["COCONUT"] + 300
                         if vol>0:
                          print("SELL", str(best_bid_amount) + "x", best_bid)
                          orders.append(Order(product, best_bid, -vol))
                          orders.append(Order("COCONUT_COUPON", best_ask, vol*15))

                       if product =="COCONUT_COUPON":
                        if int(best_ask) < -self.coupon_fair:
                         print("BUY", str(-best_ask_amount) + "x", best_ask)
                         orders.append(Order(product, best_ask, -best_ask_amount))
                        if int(best_bid) > -self.coupon_fair:
                         print("SELL", str(best_bid_amount) + "x", best_bid)
                         orders.append(Order(product, best_bid, -best_bid_amount))

            if product =="STARFRUIT":
                    if  best_ask<self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 20 - state.position["STARFRUIT"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if  best_bid>self.av2:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["STARFRUIT"] + 20
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol))  
            if product =="GIFT_BASKET":
                    if  best_ask<self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 60 - state.position["GIFT_BASKET"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if best_bid>self.av2:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["GIFT_BASKET"] + 60
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol))
            if product =="CHOCOLATE":
                    if  best_ask<self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 250 - state.position["CHOCOLATE"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if  best_bid>self.av2:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["CHOCOLATE"] + 250
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol)) 
            if product =="STRAWBERRIES":
                    if  best_bid>self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 350 - state.position["STRAWBERRIES"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if  best_bid>self.av2:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["STRAWBERRIES"] + 350
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol))
            if product =="ROSES":
                    if best_ask<self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 60 - state.position["ROSES"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if  best_bid>self.av2:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["ROSES"] + 60
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol)) 
            if product =="ORCHIDS":
                    if  self.av1>self.av2:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        vol = 20 - state.position["ORCHIDS"]
                        if vol>0:
                         orders.append(Order(product, best_ask, -vol))
                    if  (self.av1<self.av2):
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        vol = state.position["ORCHIDS"] + 20
                        if vol>0:
                         orders.append(Order(product, best_bid, -vol))              
                    
                    

            result[product] = orders
        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        if state.position["ORCHIDS"]>4:
         conversions = -2
        elif state.position["ORCHIDS"]<-4:
         conversions = 2
        else :
           conversions=None 

        return result, conversions, traderData,