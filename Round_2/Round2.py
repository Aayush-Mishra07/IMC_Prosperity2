from ast import If
import math
from datamodel import OrderDepth, UserId, TradingState, Order, ConversionObservation
from typing import List
import string
import numpy as np
import math


class Trader:
    def __init__(self):
        self.high_sunlight_values = 0
    def run(self, state: TradingState, ):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        t=state.timestamp
        conversion_observation_dict = state.observations.conversionObservations

        for product, conversion_observation in conversion_observation_dict.items():
            south_bid_price = conversion_observation.bidPrice
            south_ask_price = conversion_observation.askPrice
            humidity = conversion_observation.humidity
            sunlight = conversion_observation.sunlight
            export_tariff = conversion_observation.exportTariff
            import_tariff = conversion_observation.importTariff

            transport = conversion_observation.transportFees
        print(state.observations.conversionObservations['ORCHIDS'].bidPrice)
        print(state.observations.conversionObservations['ORCHIDS'].askPrice)
        print(state.observations.conversionObservations['ORCHIDS'].importTariff)
        print(state.observations.conversionObservations['ORCHIDS'].exportTariff)
        print(state.observations.conversionObservations['ORCHIDS'].transportFees)
        print("market Trades",state.market_trades)
        print("Own Trades",state.own_trades)
        print("position",state.position)
        exchange_acceptable = ((south_ask_price+south_bid_price)/2)-export_tariff-import_tariff-transport

        if sunlight <= 2777:
            # Append sunlight value to class variable
            self.high_sunlight_values +=1
        print("low", int(self.high_sunlight_values))
        lowsun = int(self.high_sunlight_values)
        if (lowsun > 4167)and (humidity>60) and humidity<80:#lowsunlight and ideal humidity
            n = int((lowsun - 4167) / 139)
            exchange_acceptable = exchange_acceptable * (1.04) ** n
        elif (lowsun<4167) and humidity > 80 or humidity < 60:#ideal sun and bad humidity
            n_factor = 0
            if humidity < 60:
                n_factor = int((int(humidity) - 60) / 5) * 2
            elif humidity > 80:
                n_factor = int((80 - int(humidity)) / 5) * 2

            exchange_acceptable = exchange_acceptable * (float(1) - float(n_factor / 100))
        if humidity > 80 or humidity < 60:#ideal sun and bad humidity
            n_factor = 0
            if humidity < 60:
                n_factor = int((int(humidity) - 60) / 5) * 2
            elif humidity > 80:
                n_factor = int((80 - int(humidity)) / 5) * 2

            exchange_acceptable = exchange_acceptable * (float(1) - float(n_factor / 100))
            print("exchange_acceptable",exchange_acceptable)
        south_acceptable_bid = float(exchange_acceptable) + float(export_tariff) + float(transport)
        south_acceptable_ask = float(exchange_acceptable) + float(import_tariff) + float(transport)
        print("ORCHIDS ASK",south_acceptable_ask)
        print("ORCHIDS BID",south_acceptable_bid)
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            x = int(state.timestamp)
            # print(x)
            Fs = 10000
            sine_curve = 30 * np.sin(-1 * 2 * np.pi * x / Fs)
            # Participant should calculate this value
            print("Exchange Acceptable price orchid: " + str(exchange_acceptable))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(
                len(order_depth.sell_orders)))
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if product == "STARFRUIT":
                    if int(best_ask) <= 5000:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
                elif product == "ORCHIDS":
                    if int(best_ask) <= exchange_acceptable:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                elif product == "AMETHYSTS":
                    if int(best_ask) <= 9999:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if product == "STARFRUIT":

                    if int(best_bid) >= 5000:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                elif product == "ORCHIDS":
                    if int(best_bid) >= exchange_acceptable:
                        orders.append(Order(product, best_bid, -best_bid_amount))
                elif product == "AMETHYSTS":
                    if int(best_bid) >= 10001:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))

            result[product] = orders
            print(result)

        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        if state.position.get('ORCHIDS') is not None:
         conversions= int(state.position['ORCHIDS'])
        else :
            conversions=None

        return result, conversions, traderData,


