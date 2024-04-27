from ast import If
import math

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
import math


class Trader:

    def run(self, state: TradingState):
        
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            if product == "STARFRUIT":
                acceptable_price = 5000

            else :
                acceptable_price= 10000
            x=int(state.timestamp)
            print(x)
            Fs=10000
            sine_curve=30*np.sin(-1*2 * np.pi * x / Fs)
            

            # Participant should calculate this value
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                
                if product == "STARFRUIT":
                
                    if int(best_ask) <=  -1*13*np.sin(x*((22/7)/50000)) + 5050:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
                else:
                    if int(best_ask) <= (9999):
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if product == "STARFRUIT":
                  
                      if int(best_bid) >= -1*9*np.sin(x*((22/7)/50000)) + 5050:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                else:
                    if int(best_bid) >= 10001:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))

            result[product] = orders
            print(result)

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions = 1
        return result, conversions, traderData, 
