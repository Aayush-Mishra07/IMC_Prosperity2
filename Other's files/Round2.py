from ast import If
import math

from datamodel import OrderDepth, UserId, TradingState, Order,ConversionObservation
from typing import List
import string
import numpy as np
import math


class Trader:
    def __init__(self):
        self.high_sunlight_values = []
   

    def run(self, state: TradingState, ):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        conversion_observation_dict = state.observations.conversionObservations
        
        for product, conversion_observation in conversion_observation_dict.items():
            bid_price = conversion_observation.bidPrice
            ask_price=conversion_observation.askPrice
            humidity=conversion_observation.humidity
            sunlight=conversion_observation.sunlight
            export_tariff=conversion_observation.exportTariff
            import_tariff=conversion_observation.importTariff
          
            transport=conversion_observation.transportFees
        
        if sunlight <1500:
                # Append sunlight value to class variable
                self.high_sunlight_values.append(sunlight)
        print("HIGH",len(self.high_sunlight_values))
        sizeofhigh=len(self.high_sunlight_values)
        n=0
        acceptable_orchids_bid=bid_price
        acceptable_orchids_ask=ask_price
        
        if sizeofhigh>583:
            n=int((sizeofhigh-583)/14)
            acceptable_orchids_bid=bid_price*(1.04)**n
            acceptable_orchids_ask=ask_price*(1.04)**n
        else:
            acceptable_orchids_bid=bid_price
            acceptable_orchids_ask=ask_price
        if humidity>80 or humidity<60:
            n_factor=0
            if humidity<60:
                n_factor=int((int(humidity)-60)/5)*2 
            elif humidity>80:
                 n_factor=int((80-int(humidity))/5)*2 
            acceptable_orchids_bid=bid_price*(float(1)-float(n_factor/100))
            acceptable_orchids_ask=ask_price*(float(1)-float(n_factor/100))
        acceptable_orchids_bid=float(acceptable_orchids_bid)+float(export_tariff)+float(transport)
        acceptable_orchids_ask=float(acceptable_orchids_ask)+float(import_tariff)+float(transport)
        print("ORCHIDS ASK",acceptable_orchids_ask)
        print("ORCHIDS BID",acceptable_orchids_bid)
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            if product == "STARFRUIT":
                acceptable_price = 5000

            else :
                acceptable_price= 10000
            x=int(state.timestamp)
            # print(x)
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
                
                elif product == "ORCHIDS":
                    if int(best_ask) <= acceptable_orchids_ask:
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
                elif product == "ORCHIDS":
                    if int(best_bid) >= acceptable_orchids_bid:
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
