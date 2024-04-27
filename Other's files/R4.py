from datamodel import OrderDepth, UserId, TradingState, Order, ConversionObservation
from typing import List
import string
import numpy as np
import math


class Trader:
    def __init__(self,data,timestamp) :
        self.data=[]
        self.timestamp=0
        
    def stdf(self):
        self.std_=0
        if len(self.data)>10:
            data10=self.data[-10]
            
        
            self.std_= np.std(data10)
    
        
            
    def VWAP(self,current_bid,current_offer,bid_quantity,offer_quantity):
        self.vwap=(int(current_bid)*int(offer_quantity)+int(current_offer)*int(bid_quantity))/int(int(bid_quantity)+int(offer_quantity))
        print("VWAP calculated")
     
    def BSM(self,current_bid,current_offer,bid_quantity,offer_quantity):
        Trader.VWAP(current_bid,current_offer,bid_quantity,offer_quantity)
        Trader.stdf()
        T=(int((self.timestamp))/(250*100000))
        d1=np.log(int(self.vwap)/10000)+(((float(self.std_)/100)**2)/2)*T
        self.d1=float(d1)/(float(self.std_)*float(np.sqrt(T)))
        self.d2=float(d1)-(float(self.std_)*float(np.sqrt(T)))
        print("D1 calculated",self.d1,"D")
    def couponfairprice(self):
        
       
        self.fair_buy=(self.vwap*np.random.normal(self.d1))-(10000*np.random.normal(self.d2))
        self.fair_sell=+(10000*np.random.normal(-1*self.d2))-(self.vwap*np.random.normal(-1*self.d1))
        
    def run(self, state: TradingState, ):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        best_ask_price, best_bid_price, mid_price = {}, {}, {}
        products = ['GIFT_BASKET', 'CHOCOLATE', 'STRAWBERRIES', 'ROSES','COCONUT','COCONUT_COUPON']
        for p in products:
            best_ask_price[p] = list(state.order_depths[p].sell_orders.keys())[0]
            best_bid_price[p] = list(state.order_depths[p].buy_orders.keys())[0]
            mid_price[p] = (best_ask_price[p] + best_bid_price[p]) / 2
        acceptable_gb =  6 * mid_price["CHOCOLATE"] + 4 * mid_price["STRAWBERRIES"] + mid_price["ROSES"] + 379.49
        print(f'acceptable gb:{acceptable_gb},best_ask_price {best_ask_price},best_bid_price{best_bid_price}')
     
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            self.timestamp= int(state.timestamp)
            print("timestamp",self.timestamp)
            if product=="COCONUT_COUPON":
                
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                self.data.append(best_bid)
                Trader.BSM(best_bid,best_bid_amount,best_ask,best_ask_amount)
                Trader.couponfairprice(best_bid,best_bid_amount,best_ask,best_ask_amount)
            # Fs = 10000
            # try:
            #     cpos=state.position[product]
            # except KeyError:
            #     cpos=int(0)
            # sine_curve = 30 * np.sin(-1 * 2 * np.pi * self.timestamp / Fs)
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                # if product == "STARFRUIT":
                #      if ((cpos) < 20) and (cpos < 0):
                #          num = min(40, 20 - cpos)
                       
                        

                #      if (cpos < 20) and (cpos > 15):
                #             num = min(40, 20 - cpos)
                            
                #             cpos += num

                #      if cpos < 20:
                #                 num = min(40, 20 - cpos)
                              
                #                 cpos += num
                

                #      if int(best_ask) <= 5000:
                #         print("BUY", str(-best_ask_amount) + "x", best_ask)
                #         orders.append(Order(product, best_ask, num))
                # elif product == "AMETHYSTS":
                #        if ((cpos) < 20) and (cpos < 0):
                #          num = min(40, 20 - cpos)
                       
                        

                #        if (cpos < 20) and (cpos > 15):
                #             num = min(40, 20 - cpos)
                            
                #             cpos += num

                #        if cpos < 20:
                #                 num = min(40, 20 - cpos)
                              
                #                 cpos += num
                
                    
                    
                    
                    
                #        if int(best_ask) <= 9999:
                #         print("BUY", str(-best_ask_amount) + "x", num)
                #         orders.append(Order(product, best_ask, -best_ask_amount))
                # elif product == "GIFT_BASKET":
                #        if ((cpos) < 60) and (cpos < 0):
                #             num = min(80, 60 - cpos)
                       
                        

                #        if (cpos < 60) and (cpos > 45):
                #             num = min(80, 60 - cpos)
                            
                #             cpos += num

                #        if cpos < 45:
                #                 num = min(80, 60 - cpos)
                              
                #                 cpos += num
                #        if int(best_ask) <= acceptable_gb:
                #             print("BUY", str(-best_ask_amount) + "x", best_ask)
                #             orders.append(Order(product,best_ask, -best_ask_amount))
                
                if product=="COCONUT_COUPON":
                    if float(best_ask)<float(self.fair_buy):
                        orders.append(Order(product,best_ask,-best_ask_amount))
                    


            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if product=="COCONUT_COUPON":
                    if float(best_bid)>float(self.fair_sell):
                        orders.append(Order(product,best_bid,best_bid_amount))
                # if cpos > -20:
                #     num = -20-cpos
                # if product == "STARFRUIT":
                #     if cpos > -20:
                #         num = -20-cpos
                #     if int(best_bid) >= 5000:
                #         print("SELL", str(best_bid_amount) + "x", best_bid)
                #         orders.append(Order(product, best_bid, -best_bid_amount))
                # elif product == "AMETHYSTS":
                #     if cpos > -20:
                #         num = -20-cpos
                #     if int(best_bid) >= 10001:
                #         print("SELL", str(best_bid_amount) + "x", best_bid)
                #         orders.append(Order(product, best_bid, -best_bid_amount))
                # elif product=="GIFT_BASKET":
                #     if cpos > -60:
                #         num = -60-cpos
                #     if int(best_bid) >= acceptable_gb:
                #         print("SELL", str(best_bid_amount) + "x", best_bid)
                #         orders.append(Order(product,best_bid, -best_bid_amount))



            result[product] = orders
            print(result)

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions=None

        return result, conversions, traderData,
