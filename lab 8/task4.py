import numpy as np
from itertools import product

states = ['Sunny', 'Cloudy', 'Rainy']
transition_matrix = np.array([
    [0.6, 0.3, 0.1],
    [0.4, 0.4, 0.2],
    [0.2, 0.3, 0.5]
])

def simulate_weather(days, start_state):
    current_state = states.index(start_state)
    sequence = [start_state]
    for _ in range(days-1):
        current_state = np.random.choice(len(states), p=transition_matrix[current_state])
        sequence.append(states[current_state])
    return sequence

def probability_at_least_3_rainy(days, trials=10000):
    count = 0
    for _ in range(trials):
        sequence = simulate_weather(days, 'Sunny')
        if sequence.count('Rainy') >= 3:
            count += 1
    return count/trials

weather_10_days = simulate_weather(10, 'Sunny')
prob_3_rainy = probability_at_least_3_rainy(10)

print("10-day weather simulation:", weather_10_days)
print("Probability of ≥3 rainy days:", prob_3_rainy)