import ast
import math
import collections

#===== зчитування даних =====
with open("sequence.txt", encoding="utf-8") as file:
    original_sequences = ast.literal_eval(file.read())
    original_sequences = [seq.strip("[]' ") for seq in original_sequences]

#===== RLE кодування =====
def encode_rle(sequence):
    if not sequence:
        return "", []

    result = []
    count = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1

    result.append((sequence[-1], count))

    encoded = "".join(f"{count}{char}" for char, count in result)
    return encoded, result

#===== RLE декодування =====
def decode_rle(encoded_list):
    result = []
    for char, count in encoded_list:
        result.append((char * count))
    return "".join(result)

#===== LZW кодування =====
def encode_lzw(sequence, file):
    dictionary = {chr(i): i for i in range(65536)}

    current = ""
    result = []
    total_bits = 0

    for char in sequence:
        new_str = current + char

        if new_str in dictionary:
            current = new_str
        else:
            code = dictionary[current]
            result.append(code)

            bits = 16 if code < 65536 else 17
            total_bits += bits
            file.write(f"Code: {code}, Element: {current}, bits: {bits}\n")

            dictionary[new_str] = len(dictionary)
            current = char

    if current:
        code = dictionary[current]
        result.append(code)
        bits = 16 if code < 65536 else 17
        total_bits += bits
        file.write(f"Code: {code}, Element: {current}, bits: {bits}\n")

    return result, total_bits


#===== основа =====
with open("results_rle_lzw.txt", "w", encoding="utf-8") as out:

    for idx, sequence in enumerate(original_sequences, start=1):

        out.write(f"\n===== Sequence {idx} =====\n")
        out.write(f"Original: {sequence}\n")

        N = len(sequence)
        original_bits = N * 16

        #----- статистика -----
        counts = collections.Counter(sequence)
        probability = {k: v / N for k, v in counts.items()}
        entropy = -sum(p * math.log(p) for p in probability.values())

        out.write(f"Entropy: {round(entropy, 4)}\n")
        out.write(f"Original size: {original_bits} bits\n")

        #----- RLE -----
        encoded_rle, rle_list = encode_rle(sequence)
        decoded_rle = decode_rle(rle_list)

        rle_bits = len(encoded_rle) * 16
        cr_rle = round(original_bits / rle_bits, 2) if rle_bits != 0 else 0

        if cr_rle < 1:
            cr_rle = "-"

        out.write("\n--- RLE ---\n")
        out.write(f"Encoded: {encoded_rle}\n")
        out.write(f"Decoded: {decoded_rle}\n")
        out.write(f"RLE size: {rle_bits} bits\n")
        out.write(f"Compression ratio: {cr_rle}\n")

        #----- LZW -----
        out.write("\n--- LZW ---\n")
        encoded_lzw, lzw_bits = encode_lzw(sequence, out)

        cr_lzw = round(original_bits / lzw_bits, 2) if lzw_bits != 0 else 0

        out.write(f"LZW codes: {encoded_lzw}\n")
        out.write(f"LZW size: {lzw_bits} bits\n")
        out.write(f"Compression ratio: {cr_lzw}\n")

    print("Результати збережено у файлі results_rle_lzw.txt")