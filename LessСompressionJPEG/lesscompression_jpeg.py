import os
import numpy as np
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree

#--- DCT ---

def dct_2d(image):
    return fftpack.dct(
        fftpack.dct(image.T, norm='ortho').T,
        norm='ortho',
    )

def idct_2d(image):
    return fftpack.dct(
        fftpack.dct(image.T, norm='ortho').T,
        norm='ortho',
    )


#--- quantization ---
def load_quantization_table(component):

    if component == 'lum':
        return np.array([
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ])

    elif component == 'chrom':
        return np.array([
            [17, 18, 24, 47, 99, 99, 99, 99],
            [18, 21, 26, 66, 99, 99, 99, 99],
            [24, 26, 56, 99, 99, 99, 99, 99],
            [47, 66, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99]
        ])

def quantize(blok, component):
    q = load_quantization_table(component)
    return (blok / q).round().astype(np.int32)

def dequantize(blok, component):
    q = load_quantization_table(component)
    return blok * q


#--- zigzag ---
def zigzag_points(rows, cols):

    solution = [[] for _ in range(rows + cols - 1)]

    for i in range(rows):
        for j in range(cols):

            s = i + j

            if s % 2 == 0:
                solution[s].insert(0, (i, j))
            else:
                solution[s].append((i, j))

    for diagonal in solution:
        for point in diagonal:
            yield point


def block_to_zigzag(block):

    return np.array(
        [block[point] for point in zigzag_points(*block.shape)]
    )


def zigzag_to_block(zigzag):

    block = np.empty((8, 8), np.int32)

    for i, point in enumerate(zigzag_points(8, 8)):
        block[point] = zigzag[i]

    return block



#--- RLE ---
def run_length_encode(arr):

    encoded = []

    count = 1
    prev = arr[0]

    for elem in arr[1:]:

        if elem == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = elem
            count = 1

    encoded.append((prev, count))
    return encoded


#--- encode ---
def encode(input_file, output_file):

    image = Image.open(input_file)

    ycbcr = image.convert('YCbCr')

    npmat = np.array(ycbcr, dtype=np.uint8)

    rows, cols = npmat.shape[0], npmat.shape[1]

    if rows % 8 != 0 or cols % 8 != 0:
        raise ValueError(
            "Ширина та висота мають бути кратними 8"
        )

    result = []

    for row in range(0, rows, 8):
        for col in range(0, cols, 8):
            for channel in range(3):

                block = npmat[row:row + 8, col:col + 8, channel]

                block = block.astype(np.int32) - 128

                dct_block = dct_2d(block)

                quant_block = quantize(
                    dct_block,
                    'lum' if channel == 0 else 'chrom'
                )

                zigzag = block_to_zigzag(quant_block)

                rle = run_length_encode(zigzag)

                result.extend(rle)


#--- huffman ---
    values = []

    for item in result:
        values.append(item)

    huffman = HuffmanTree(values)

    table = huffman.value_to_bitstring_table()

    encoded_bits = ""

    for item in result:
        encoded_bits += table[item]

    with open(output_file, 'w') as f:
        f.write(encoded_bits)

    print("Кодування завершено")
    print("Розмір після стиснення:", len(encoded_bits), "біт")


#--- decode ---
def decoder(input_image, restored_image):

    image = Image.open(input_image)

    image = image.convert('YCbCr')

    npmat = np.array(image, dtype=np.uint8)

    rows, cols = npmat.shape[0], npmat.shape[1]

    restored = np.zeros_like(npmat)

    for row in range(0, rows, 8):
        for col in range(0, cols, 8):
            for channel in range(3):
                block = npmat[row:row + 8, col:col + 8, channel]
                block = block.astype(np.int32) - 128
                dct_block = dct_2d(block)

                quant_block = quantize(
                    dct_block,
                    'lum' if channel == 0 else 'chrom'
                )

                dequant_block = dequantize(
                    quant_block,
                    'lum' if channel == 0 else 'chrom'
                )

                restored_block = idct_2d(dequant_block)

                restored_block = restored_block + 128

                restored_block = np.clip(
                    restored_block,
                    0,
                    255
                )

                restored[row:row + 8,
                         col:col + 8,
                         channel] = restored_block

        restored_img = Image.fromarray(
            restored.astype(np.uint8),
        ).convert('RGB')

        restored_img.save(restored_image)




#--- main ---
if __name__ == "__main__":

    input_file = "image.jpg"

    output_file = "compressed.asf"

    restored_file = "restored.jpg"

    encode(input_file, output_file)

    decoder(input_file, restored_file)

print("Декодування завершено")