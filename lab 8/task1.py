from itertools import product

faces = [1, 2, 3, 4, 5, 6]
evens = [2, 4, 6]
pe = len(evens) / len(faces)
gt4 = [5, 6]
pg = len(gt4) / len(faces)
lt3 = [1, 2]
pl = len(lt3) / len(faces)



# 2 dices
def sum_ge7():
    c = 0
    for d1 in range(1,7):
        for d2 in range(1,7):
            if d1+d2 >=7:
                c+=1
    return c

def sum_eq8():
    c = 0
    for d1 in range(1,7):
        for d2 in range(1,7):
            if d1+d2 ==8:
                c+=1
    return c

def cond_odd():
    return 2*3

total = 36
ps7 = sum_ge7()/total
ps8 = sum_eq8()/total
first_gt4 = 12
second_odd = cond_odd()
pc = second_odd/first_gt4

print("Single die probabilities:")
print(f"Even: {pe:.2f} or {pe:.2%}")
print(f">4: {pg:.2f} or {pg:.2%}")
print(f"<3: {pl:.2f} or {pl:.2%}")

print("\nTwo dice probabilities:")
print(f"Sum≥7: {ps7:.4f} or {ps7:.2%}")
print(f"Sum=8: {ps8:.4f} or {ps8:.2%}")
print(f"Odd|>4: {pc:.2f} or {pc:.2%}")