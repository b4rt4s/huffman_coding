import math

with open('skompresowany.txt', 'rb') as file:
    compressed_text = [i for i in file.read()]

    uniq_signs_count = compressed_text[0]

    dictionary = [chr(compressed_text[i]) for i in range(1, uniq_signs_count + 1)]

    list_to_decompress = [bin(compressed_text[i])[2:].zfill(8)
                          for i in range(uniq_signs_count + 1, len(compressed_text))]

    bin_text = ''.join(list_to_decompress)

    to_decompress = bin_text[3:len(bin_text)-(int(bin_text[:3], 2))]

    N = math.ceil(math.log2(uniq_signs_count))

    decompressed = [dictionary[int(to_decompress[i:i+N], 2)]
                    for i in range(0, len(to_decompress), N)]

    with open('zdekompresowany.txt', 'w') as file2:
        file2.write(''.join(decompressed))
