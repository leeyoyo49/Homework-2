# Define the liquidity pools
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}


def get_amount_out(amount_in, reserve_in, reserve_out):
    # Uniswap V2 uses a 0.3% fee, so we need to account for that
    fee = 0.003
    amount_in_with_fee = amount_in * (1 - fee)
    amount_out = amount_in_with_fee * reserve_out / (reserve_in + amount_in_with_fee)
    return amount_out

def swap_tokens(liquidity, from_token, to_token, amount):
    # Check if the pool exists for the token pair
    if (from_token, to_token) in liquidity:
        reserve_from, reserve_to = liquidity[(from_token, to_token)]
    elif (to_token, from_token) in liquidity:
        reserve_to, reserve_from = liquidity[(to_token, from_token)]
    else:
        return {"error": "No liquidity pool exists for this token pair"}

    # Calculate the amount of to_token that will be received
    amount_out = get_amount_out(amount, reserve_from, reserve_to)

    # Update the liquidity pool reserves
    new_reserve_from = reserve_from + amount
    new_reserve_to = reserve_to - amount_out

    # Update the liquidity dictionary
    if (from_token, to_token) in liquidity:
        liquidity[(from_token, to_token)] = (new_reserve_from, new_reserve_to)
    else:
        liquidity[(to_token, from_token)] = (new_reserve_to, new_reserve_from)

    # Return the amount of to_token received and the updated liquidity pool
    return {
        "amount_out": amount_out,
        "updated_liquidity": liquidity
    }


from collections import deque

def BFS(liquidity, from_token, to_token, amount_in, target_amount):
    # Initialize the queue with the starting point and initial liquidity
    queue = deque([(from_token, amount_in, [from_token], liquidity)])
    best_amount = 0
    best_route = []

    while queue:
        current_token, current_amount, current_path, current_liquidity = queue.popleft()

        # Check if we have reached or exceeded the target amount
        if current_token == to_token and current_amount >= target_amount:
            if current_amount > best_amount:  # Update the best route if a better one is found
                best_amount = current_amount
                best_route = current_path
                break
            continue

        # Explore the neighbors
        for (token1, token2) in current_liquidity.keys():
            if token1 == current_token:
                next_token = token2
            elif token2 == current_token:
                next_token = token1
            else:
                continue

            swap_result = swap_tokens(current_liquidity.copy(), current_token, next_token, current_amount)
            if "error" not in swap_result:
                new_amount_out = swap_result["amount_out"]
                new_liquidity = swap_result["updated_liquidity"]
                new_path = current_path + [next_token]
                queue.append((next_token, new_amount_out, new_path, new_liquidity))

    return best_amount, best_route

best_amount, best_route = BFS(liquidity, "tokenB", "tokenB", 5, 20)
print("path: ", end='')
for i in range(len(best_route)-1):
    print(best_route[i], end='->')
print(best_route[-1], end='')
print(", tokenB balance=", best_amount, end='.', sep='')

# result= swap_tokens(liquidity, "tokenB", "tokenA", 5)
# print(result)
# result= swap_tokens(result["updated_liquidity"], "tokenA", "tokenD", result["amount_out"])
# print(result)
# result= swap_tokens(result["updated_liquidity"], "tokenD", "tokenC", result["amount_out"])
# print(result)
# result= swap_tokens(result["updated_liquidity"], "tokenC", "tokenB", result["amount_out"])
# print(result)