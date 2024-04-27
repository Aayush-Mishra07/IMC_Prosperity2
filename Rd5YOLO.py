from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string


class Trader:
    def __init__(self) -> None:
     self.def_pos = {'COCONUT_COUPON' : 0, 'COCONUT' : 0, 'AMETHYSTS' : 0,'CHOCOLATE':0,'STRAWBERRIES':0,'ROSES':0,'STARFRUIT':0,'ORCHIDS':0,"GIFT_BASKET":0}
    
    def run(self, state: TradingState):

        print("traderData:", state.traderData)
        print("Observations:", state.observations)
        print("position size:", state.position)
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            if len(order_depth.sell_orders) != 0:
                 best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                 worst_ask,worst_ask_amount = (list(order_depth.sell_orders.items())[::-1])[0]
            if len(order_depth.buy_orders) != 0:
                 best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                 worst_bid, worst_bid_amount = (list(order_depth.buy_orders.items())[::-1])[0]
            if product!="ORCHIDS":     
             if product == "AMETHYSTS":
                         state.position[product]=self.def_pos[product]
             if product =="AMETHYSTS":
                    if int(best_ask) < 10000:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
                    if int(best_bid) > 10000:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
             else:             
            # Access market trades if available
              market_trade = state.market_trades.get(product)
              if market_trade:
                mp = market_trade[0].price
                mb = market_trade[0].buyer
                ms = market_trade[0].seller
                mq = market_trade[0].quantity
                if mb =="Valentina" and product=="COCONUT_COUPON" or product=="STARFRUIT":
                    orders.append(Order(product,int(mp+2),-mq))
                    orders.append(Order(product,int(mp-2),mq))
                
                if mb =="Vinnie" and product == "COCONUT":
                    orders.append(Order(product,int(mp),-mq))
                    orders.append(Order(product,int(mp-1),mq))
                if ms == "Vinnie" and product =="COCONUT":
                    orders.append(Order(product,int(mp),mq)) 
                    orders.append(Order(product,int(mp+1),-mq))  
                if mb =="Vinnie"and ms=="Vladimir":
                   orders.append(Order("STRAWBERRIES",int(mp-1),mq))           
                if mb=="Ruby" and product=="GIFT_BASKET":
                    orders.append(Order(product,int(mp+5),-mq))
                    orders.append(Order(product,int(mp-5),mq)) 
                elif ms=="Rhianna" :
                    orders.append(Order(product,int(mp+1),mq)) 
                    orders.append(Order(product,int(mp+3),-mq))                   

            
             own_trade = state.own_trades.get(product)
             if own_trade:
                op = own_trade[0].price
                ob = own_trade[0].buyer
                os = own_trade[0].seller
                oq = own_trade[0].quantity
                if ob=="SUBMISSION" and state.position[product]>0:
                 orders.append(Order(product, int(op + 1.0), -oq))
                if os=="SUBMISSION" and state.position[product]<0:
                 orders.append(Order(product, int(op - 1.0), oq)) 
            
            result[product] = orders

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        conversions = None
        return result, conversions, traderData
