from datamodel import OrderDepth, UserId, TradingState, Order, ConversionObservation
from typing import List
import string
import numpy as np
import math


class Trader:

    def run(self, state: TradingState, ):
        if state.position =={}:
            state.position = {'GIFT_BASKET' : 0, 'COCONUT_COUPON' : 0, 'COCONUT' : 0, 'AMETHYST' : 0}
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        best_ask_price, best_bid_price, mid_price = {}, {}, {}
        buy_signal,sell_signal,buy_signal_gb,sell_signal_gb =0,0,0,0


        products = ['GIFT_BASKET', 'CHOCOLATE', 'STRAWBERRIES', 'ROSES','COCONUT','COCONUT_COUPON']
        for p in products:
            best_ask_price[p] = list(state.order_depths[p].sell_orders.keys())[0]
            best_bid_price[p] = list(state.order_depths[p].buy_orders.keys())[0]
            mid_price[p] = (best_ask_price[p] + best_bid_price[p]) / 2
        sig_gb =  mid_price["GIFT_BASKET"] - 6 * mid_price["CHOCOLATE"] - 4 * mid_price["STRAWBERRIES"] - mid_price["ROSES"] - 379.49
        spread = mid_price["COCONUT_COUPON"]-mid_price["COCONUT"]
        if sig_gb > (76.4243*0.75):
            sell_signal_gb=1
        if sig_gb<(-76.4243*0.75):
            buy_signal_gb=1
        if spread < -9364.85455 - (46.108*0.75):
            buy_signal =1
        if spread > -9364.855 + (46.108*0.75):
            sell_signal = 1
        print(f'best_ask_price {best_ask_price["COCONUT_COUPON"]},best_bid_price{best_bid_price["COCONUT_COUPON"]}')
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            x = int(state.timestamp)
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                worst_ask,worst_ask_amount = (list(order_depth.sell_orders.items())[::-1])[0]
            if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    worst_bid, worst_bid_amount = (list(order_depth.buy_orders.items())[::-1])[0]
            if product == "AMETHYSTS":
                    if int(best_ask) <= 10000:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
                    if int(best_bid) >= 10000:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))

            if product == "COCONUT_COUPON":
                    if buy_signal==1:
                            orders.append(Order(product, best_ask,best_ask_amount))
                            orders.append(Order("COCONUT", best_bid, -best_ask_amount))
                    if sell_signal==1:
                            orders.append(Order(product, best_bid, -best_bid_amount))
                            orders.append(Order("COCONUT", best_ask, best_bid_amount))
            if product == "GIFT_BASKET":
                    if buy_signal_gb == 1:
                            orders.append(Order(product, best_ask,best_ask_amount))
                            orders.append(Order("STRAWBERRIES", best_ask,-6*best_ask_amount))
                            orders.append(Order("CHOCOLATE", best_ask,- 4*best_ask_amount))
                            orders.append(Order("ROSES", best_ask, -1*best_ask_amount))
                    if sell_signal_gb==1:
                            orders.append(Order(product, best_bid, -best_bid_amount))
                            orders.append(Order("STRAWBERRIES", best_bid, (best_bid_amount*6)))
                            orders.append(Order("CHOCOLATE", best_bid, (best_bid_amount*4)))
                            orders.append(Order("ROSES", best_bid, best_bid_amount))





            result[product] = orders
            print(result)

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions=None

        return result, conversions, traderData,



