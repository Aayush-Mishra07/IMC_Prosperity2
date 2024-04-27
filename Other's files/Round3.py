from datamodel import OrderDepth, UserId, TradingState, Order, ConversionObservation
from typing import List
import string
import numpy as np
import math


class Trader:
    def run(self, state: TradingState, ):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        best_ask_price, best_bid_price, mid_price = {}, {}, {}
        products = ['GIFT_BASKET', 'CHOCOLATE', 'STRAWBERRIES', 'ROSES']
        for p in products:
            best_ask_price[p] = list(state.order_depths[p].sell_orders.keys())[0]
            best_bid_price[p] = list(state.order_depths[p].buy_orders.keys())[0]
            mid_price[p] = (best_ask_price[p] + best_bid_price[p]) / 2
        acceptable_gb =  6 * mid_price["CHOCOLATE"] + 4 * mid_price["STRAWBERRIES"] + mid_price["ROSES"] + 379.49
        print(f'acceptable gb:{acceptable_gb},best_ask_price {best_ask_price},best_bid_price{best_bid_price}')
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            x = int(state.timestamp)
            # print(x)
            Fs = 10000
            try:
                cpos=float(state.position[product])
            except KeyError:
                cpos=0
            sine_curve = 30 * np.sin(-1 * 2 * np.pi * x / Fs)
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if product == "STARFRUIT":
                     if ((cpos) < 20) and (float(state.position[product]) < 0):
                         num = min(40, 20 - cpos)
                       
                        

                     if (cpos < 20) and (float(state.position[product]) > 15):
                            num = min(40, 20 - cpos)
                            
                            cpos += num

                     if cpos < 20:
                                num = min(40, 20 - cpos)
                              
                                cpos += num
                

                     if int(best_ask) <= 5000:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, num))
                elif product == "AMETHYSTS":
                       if ((cpos) < 20) and (float(state.position[product]) < 0):
                         num = min(40, 20 - cpos)
                       
                        

                       if (cpos < 20) and (float(state.position[product]) > 15):
                            num = min(40, 20 - cpos)
                            
                            cpos += num

                       if cpos < 20:
                                num = min(40, 20 - cpos)
                              
                                cpos += num
                
                    
                    
                    
                    
                       if int(best_ask) <= 9999:
                        print("BUY", str(-best_ask_amount) + "x", num)
                        orders.append(Order(product, best_ask, -best_ask_amount))
                elif product == "GIFT_BASKET":
                       if ((cpos) < 60) and (float(state.position[product]) < 0):
                            num = min(40, 20 - cpos)
                       
                        

                       if (cpos < 60) and (float(state.position[product]) > 45):
                            num = min(60, 60 - cpos)
                            
                            cpos += num

                       if cpos < 20:
                                num = min(800, 60 - cpos)
                              
                                cpos += num
                       if int(best_ask) <= acceptable_gb:
                            print("BUY", str(-best_ask_amount) + "x", best_ask)
                            orders.append(Order(product,best_ask, -best_ask_amount))


            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if cpos > -20:
                    num = -20-cpos
                if product == "STARFRUIT":
                    if cpos > -20:
                        num = -20-cpos
                    if int(best_bid) >= 5000:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                elif product == "AMETHYSTS":
                    if cpos > -20:
                        num = -20-cpos
                    if int(best_bid) >= 10001:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                elif product=="GIFT_BASKET":
                    if cpos > -60:
                        num = -60-cpos
                    if int(best_bid) >= acceptable_gb:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product,best_bid, -best_bid_amount))



            result[product] = orders
            print(result)

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions=None

        return result, conversions, traderData,
