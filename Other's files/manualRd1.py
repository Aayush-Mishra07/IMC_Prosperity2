price_tuples = [(price, price - 900) for price in range(900, 1001)]

max_value = float('-inf')
max_x1 = None
max_x2 = None

for x1 in range(900, 1001):
    for x2 in range(x1, 1001):
        total_sum = 0
        for price, diff in price_tuples:
            if price < x1:
                total_sum += (1000-x1) * diff
            elif x1 <= price < x2:
                total_sum += (1000-x2) * diff
        if total_sum > max_value:
            max_value = total_sum
            max_x1 = x1
            max_x2 = x2

print("Maximum value:", max_value)
print("x1 value:", max_x1)
print("x2 value:", max_x2)
