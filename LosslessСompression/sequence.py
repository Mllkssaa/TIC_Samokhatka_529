import random
import string
import collections
import math
import os
import matplotlib.pyplot as plt

#параметри
N_sequence = 100
surname = "Samokhatka"
group = "529"
student_number = 13

#створ папки
if not os.path.exists("LosslessComparison"):
    os.makedirs("LosslessComparison")

#==========ГЕНЕРАЦІЯ ПОСЛІДОВНОСТЕЙ==========

#1
list1 = ['1'] * student_number
list0 = ['0'] * (N_sequence - student_number)
seq1 = list1 + list0
random.shuffle(seq1)
seq1 = ''.join(seq1)

#2
seq2 = surname + '0' * (N_sequence - len(surname))

#3
list_mix = list(surname) + ['0'] * (N_sequence - len(surname))
random.shuffle(list_mix)
seq3 = ''.join(list_mix)

#4
letters = list(surname) + list(group)
n_letters = len(letters)
n_repeats = N_sequence // n_letters
remainder = N_sequence % n_letters
seq4_list = letters * n_repeats + letters[:remainder]
seq4 = ''.join(seq4_list)

#5
elements5 = list(surname[:2])
seq5 = ''.join(random.choices(elements5, k=N_sequence))

#6
letters6 = list(surname[:2])
digits6 = list(group)

n_letters6 = int(0.7 * N_sequence)
n_digits6 = N_sequence - n_letters6

seq6_list = [random.choice(letters6) for _ in range(n_letters)] + \
            [random.choice(digits6) for _ in range(n_digits6)]
random.shuffle(seq6_list)
seq6 = ''.join(seq6_list)

#7
elements7 = string.ascii_lowercase + string.digits
seq7 = ''.join(random.choice(elements7) for _ in range(N_sequence))

#8
seq8 = '1' * N_sequence

#список
sequences = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]

#=====АНАЛІЗ=====

results = []

with open("LosslessComparison/results_sequence.txt", "a", encoding="utf-8") as file:

    for i, sequence in enumerate(sequences, 1):

        alphabet = set(sequence)
        alphabet_size = len(alphabet)

        #розмір
        size_bytes = len(sequence)
        size_bits = len(sequence) * 8

        #ймовірність
        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}

        mean_probability = sum(probability.values()) / len(probability)
        equal = all(abs(p - mean_probability) <0.1 * mean_probability for p in probability.values())
        uniformity = "рівна" if equal else "нерівна"

        #ентропія
        entropy = -sum(p * math.log2(p) for p in probability.values())

        #надмірність
        if alphabet_size > 1:
            redundancy = 1 - entropy / math.log2(alphabet_size)
        else:
            redundancy = 1

        #запис
        prob_str = ', '.join([f"{k}={v:.4f}" for k, v in probability.items()])

        file.write(f"\n---Sequence {i}---\n")
        file.write(f"{sequence}\n")
        file.write(f"Alphabet size: {alphabet_size}\n")
        file.write(f"Size: {size_bytes} bytes ({size_bits} bits)\n")
        file.write(f"Probability: {prob_str}\n")
        file.write(f"Mean probability: {mean_probability:.4f}\n")
        file.write(f"Type: {uniformity}\n")
        file.write(f"Entropy: {entropy:.4f}\n")
        file.write(f"Redundancy: {redundancy:.4f}\n")

        results.append([
            alphabet_size,
            round(entropy, 2),
            round(redundancy, 2),
            uniformity
        ])


#==========ЗБЕРЕЖЕНННЯ ПОСЛІДОВНОСТЕЙ==========

with open("LosslessComparison/results_sequence.txt", "a") as f:
    for seq in sequences:
        f.write(seq + "\n")


#=====ТАБЛИЦЯ=====

headers = ['Alphabet size', 'Entropy', 'Redundancy', 'Probability']
rows = [f"Seq {i}" for i in range(1, 9)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')

table = ax.table(
    cellText=results,
    colLabels=headers,
    rowLabels=rows,
    loc='center',
    cellLoc='center',
)

table.set_fontsize(12)
table.scale(1, 2)

fig.savefig("LosslessComparison/results_sequence.png", dpi=300)
plt.close()

print("Практична робота №5. Результат збережено в папку LosslessComparison")