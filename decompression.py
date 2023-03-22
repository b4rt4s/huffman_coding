import math

with open('skompresowany.txt', 'rb') as file:
    decrypted_text = [i for i in file.read()]

    print(decrypted_text)

    main_tab = []

    for k in range(256):
        tab = []

        for i in range(256):
            if i + k > 255:
                tab.append(i + k - 256)
            else:
                tab.append((i + k))

        main_tab.append(tab)

    key = input('Input your key: ')

    j = 0

    tab_dencrypt = []

    for x in decrypted_text:
        key_sign = ord(key[j])

        print(key_sign)

        sign = x

        print(x)

        print(main_tab[key_sign])

        print('')

        tab_dencrypt.append(main_tab[key_sign].index(sign))

        j = (j + 1) % len(key)

    # ----------------------

    print(tab_dencrypt)

    compressed_text = tab_dencrypt

    uniq_signs_count = compressed_text[0]

    print(uniq_signs_count)

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
