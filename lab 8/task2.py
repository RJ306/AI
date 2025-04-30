from fractions import Fraction

total = 52

red = 26 
p_red = Fraction(red, total)

hearts = 13
p_heart_given_red = Fraction(hearts, red)

face_cards = 12  
diamond_faces = 3
p_diamond_given_face = Fraction(diamond_faces, face_cards)

spade_faces = 3
queens = 4  # one per suit
spade_or_queen_faces = spade_faces + queens - 1  # -1 to avoid double counting of queen
p_spade_or_queen_given_face = Fraction(spade_or_queen_faces, face_cards)

print("Card Probabilities:")
print(f"1. P(Red) = {p_red} ≈ {float(p_red):.2%}")
print(f"2. P(Heart|Red) = {p_heart_given_red} ≈ {float(p_heart_given_red):.2%}")
print(f"3. P(Diamond|Face) = {p_diamond_given_face} ≈ {float(p_diamond_given_face):.2%}")
print(f"4. P(Spade or Queen|Face) = {p_spade_or_queen_given_face} ≈ {float(p_spade_or_queen_given_face):.2%}")