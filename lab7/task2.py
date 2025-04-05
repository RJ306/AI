MAXIMUM = float('inf')
MINIMUM = float('-inf')

def calculate(coins, is_max, alpha, beta):
    if not coins:
        return 0
    
    if is_max:
        left = coins[0] + calculate(coins[1:], False, alpha, beta)
        right = coins[-1] + calculate(coins[:-1], False, alpha, beta)
        best = max(left, right)
        alpha = max(alpha, best)
        if beta <= alpha:
            return best
        return best
    else:
        if coins[0] < coins[-1]:
            return calculate(coins[1:], True, alpha, beta)
        else:
            return calculate(coins[:-1], True, alpha, beta)

def play(coins):
    max_score = 0
    min_score = 0
    turn = True
    current = coins.copy()
    
    while current:
        if turn:
            left_val = current[0] + calculate(current[1:], False, MINIMUM, MAXIMUM)
            right_val = current[-1] + calculate(current[:-1], False, MINIMUM, MAXIMUM)
            if left_val >= right_val:
                pick = current.pop(0)
            else:
                pick = current.pop()
            max_score += pick
            print(f"Max picks {pick}, Remaining: {current}")
        else:
            if current[0] < current[-1]:
                pick = current.pop(0)
            else:
                pick = current.pop()
            min_score += pick
            print(f"Min picks {pick}, Remaining: {current}")
        turn = not turn
    
    print(f"\nFinal Scores - Max: {max_score}, Min: {min_score}")
    if max_score > min_score:
        print("Winner: Max")
    elif min_score > max_score:
        print("Winner: Min")
    else:
        print("Tie")

coins = [3, 9, 1, 2, 7, 5]
print("Start Coins:", coins)
play(coins)