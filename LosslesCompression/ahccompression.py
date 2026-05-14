import math
import collections
import ast

# =========================
# FLOAT → BINARY
# =========================
def float_bin(point, size_cod):
    binary_code = ""
    for _ in range(size_cod):
        point *= 2
        if point >= 1:
            binary_code += "1"
            point -= 1
        else:
            binary_code += "0"
    return binary_code


# =========================
# ARITHMETIC ENCODING
# =========================
def encode_ac(uniq_chars, probabilitys, sequence):
    alphabet = sorted(list(uniq_chars))
    probability = [probabilitys[s] for s in alphabet]

    # cumulative intervals
    unity = []
    low = 0.0

    for i in range(len(alphabet)):
        high = low + probability[i]
        unity.append([alphabet[i], low, high])
        low = high

    for symbol in sequence[:-1]:
        for i in range(len(unity)):
            if unity[i][0] == symbol:
                low, high = unity[i][1], unity[i][2]
                diff = high - low

                new_unity = []
                start = low

                for j in range(len(unity)):
                    new_low = start
                    new_high = start + probability[j] * diff
                    new_unity.append([unity[j][0], new_low, new_high])
                    start = new_high

                unity = new_unity
                break

    # last symbol interval
    for i in range(len(unity)):
        if unity[i][0] == sequence[-1]:
            low, high = unity[i][1], unity[i][2]
            break

    point = (low + high) / 2
    diff = max(high - low, 1e-12)

    size_cod = math.ceil(math.log2(1 / diff) + 1)
    bin_code = float_bin(point, size_cod)

    return [point, alphabet, probability], bin_code


# =========================
# ARITHMETIC DECODING
# =========================
def decode_ac(encoded_data, length):
    point, alphabet, probability = encoded_data

    unity = []
    low = 0.0

    for i in range(len(alphabet)):
        high = low + probability[i]
        unity.append([alphabet[i], low, high])
        low = high

    result = ""

    for _ in range(length):
        for i in range(len(unity)):
            if unity[i][1] <= point < unity[i][2]:
                symbol = unity[i][0]
                result += symbol

                low, high = unity[i][1], unity[i][2]
                diff = high - low

                new_unity = []
                start = low

                for j in range(len(unity)):
                    new_low = start
                    new_high = start + probability[j] * diff
                    new_unity.append([unity[j][0], new_low, new_high])
                    start = new_high

                unity = new_unity
                break

    return result


# =========================
# HUFFMAN ENCODING
# =========================
def encode_ch(uniq_chars, probabilitys, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[s] for s in alphabet]

    nodes = [[p, [s, ""]] for s, p in zip(alphabet, probability)]
    nodes.sort()

    while len(nodes) > 1:
        lo = nodes.pop(0)
        hi = nodes.pop(0)

        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]

        nodes.append([lo[0] + hi[0]] + lo[1:] + hi[1:])
        nodes.sort()

    huffman_dict = dict(nodes[0][1:])

    encoded = "".join(huffman_dict[c] for c in sequence)

    symbol_code = [[k, v] for k, v in huffman_dict.items()]

    return [encoded, symbol_code], encoded


# =========================
# HUFFMAN DECODING
# =========================
def decode_ch(encoded_data):
    encoded, symbol_code = encoded_data
    reverse = {code: sym for sym, code in symbol_code}

    temp = ""
    result = ""

    for bit in encoded:
        temp += bit
        if temp in reverse:
            result += reverse[temp]
            temp = ""

    return result


# =========================
# MAIN
# =========================
def main():
    import matplotlib.pyplot as plt

    with open("sequence.txt", "r") as file:
        sequences = ast.literal_eval(file.read())

    entropies = []
    bps_ac_list = []
    bps_ch_list = []
    labels = []

    with open("result_AC_CH.txt", "w", encoding="utf-8") as f:

        for idx, sequence in enumerate(sequences):
            sequence = sequence.strip().replace(" ", "")

            if len(set(sequence)) == 1:
                continue

            N = len(sequence)

            counts = collections.Counter(sequence)
            probability = {s: counts[s] / N for s in counts}

            entropy = -sum(p * math.log2(p) for p in probability.values())

            # AC
            data_ac, encoded_ac = encode_ac(set(sequence), probability, sequence)
            decoded_ac = decode_ac(data_ac, N)
            bps_ac = len(encoded_ac) / N

            #Huffman
            data_ch, encoded_ch = encode_ch(set(sequence), probability, sequence)
            decoded_ch = decode_ch(data_ch)
            bps_ch = len(encoded_ch) / N

            #запис у файл
            f.write(f"\n=== Sequence {idx+1} ===\n")
            f.write(f"Original: {sequence}\n")
            f.write(f"Entropy: {entropy:.4f}\n")

            f.write(f"AC Encoded: {encoded_ac}\n")
            f.write(f"AC Decoded: {decoded_ac}\n")
            f.write(f"BPS AC: {bps_ac:.4f}\n")

            f.write(f"\nCH Encoded: {encoded_ch}\n")
            f.write(f"CH Decoded: {decoded_ch}\n")
            f.write(f"BPS CH: {bps_ch:.4f}\n")

            #збереження для графіків
            entropies.append(entropy)
            bps_ac_list.append(bps_ac)
            bps_ch_list.append(bps_ch)
            labels.append(f"S{idx + 1}")

            #графік 1 (послідовності)
            plt.figure()

            plt.plot(labels, entropies, marker='o', label='Entropy')
            plt.plot(labels, bps_ac_list, marker='o', label='AC (bps)')
            plt.plot(labels, bps_ch_list, marker='o', label='Huffman (bps)')

            plt.title("Entropy vs Compression Methods")
            plt.xlabel("Sequences")
            plt.ylabel("Bits per symbol (bps)")
            plt.legend()
            plt.grid()

            plt.show()

            #графік 2 (середні значення)
            plt.figure()

            methods = ["Entropy", "AC", "Huffman"]
            values = [
                sum(entropies) / len(entropies),
                sum(bps_ac_list) / len(bps_ac_list),
                sum(bps_ch_list) / len(bps_ch_list)
            ]

            plt.bar(methods, values)

            plt.title("Average Compression Efficiency")
            plt.ylabel("Bits per symbol")
            plt.grid(axis='y')

            plt.show()

            #графік 3 (надлишковість)
            plt.figure()

            diff_ac = [a - e for a, e in zip(bps_ac_list, entropies)]
            diff_ch = [c - e for c, e in zip(bps_ch_list, entropies)]

            plt.plot(labels, diff_ac, marker='o', label='AC - Entropy')
            plt.plot(labels, diff_ch, marker='o', label='Huffman - Entropy')

            plt.title("Coding Redundancy")
            plt.xlabel("Sequences")
            plt.ylabel("Extra bits over entropy")
            plt.legend()
            plt.grid()

            plt.show()


if __name__ == "__main__":
    main()