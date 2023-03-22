import math

with open('skompresowany.txt', 'rb') as file:
    # odczyt pliku jako listy wartosci decymalnych poszczegolnych znakow
    text = [i for i in file.read()]

# -----------------
#   DESZYFROWANIE
# -----------------

# zainicjowanie rozszerzonej tablicy ASCII o zakresie znakow od 0 do 255
tab_of_ascii_lists = [[col + row - 256 if col + row > 255 else col + row
                       for col in range(256)] for row in range(256)]

key = input('Podaj klucz: ')

# zabezpieczenie na wypadek nie podania klucza
if len(key) == 0:
    print('Bez podania klucza dekompresja jest niemozliwa!')
    exit()

j = 0

dencrypted_text = []

# deszyfrowanie skompresowanego tekstu
for char in text:
    # decymalna wartość danego znaku klucza
    key_sign = ord(key[j])

    # zapisanie do tablicy odszyfrowanych znaków skompresowanego tekstu
    dencrypted_text.append(tab_of_ascii_lists[key_sign].index(char))

    # resetowanie indeksu znaku w kluczu, gdyby byl on krotszy niz tekst do odszyfrowania
    j = (j + 1) % len(key)

# -----------------
#    DEKOMPRESJA
# -----------------

compressed_text = dencrypted_text

# pobranie informacji o ilości typow znakow wystepujacych w tekscie
uniq_signs_count = compressed_text[0]

# pobranie listy typow znakow wystepujacych w tekscie
dictionary = [chr(compressed_text[i]) for i in range(1, uniq_signs_count + 1)]

# zamiana znakow do dekompresji z systemu decymalnego na binarny
list_to_decompress = [bin(compressed_text[i])[2:].zfill(8)
                      for i in range(uniq_signs_count + 1, len(compressed_text))]

bin_text = ''.join(list_to_decompress)

redundant_bits = int(bin_text[:3], 2)

# wyciecie z tekstu binarnego pierwszych trzech bitow informujacych
# o ilosci bitow nadmiarowych oraz wyciecie tych bitow nadmiarowych
to_decompress = bin_text[3:(len(bin_text) - redundant_bits)]

# obliczenie minimalnej ilosci bitow potrzebnej na zakodowanie jednego znaku w tekscie
N = math.ceil(math.log2(uniq_signs_count))

k = 0
with open('zdekompresowany.txt', 'w') as file:
    # dekompresja tekstu i zapisanie go na liscie str
    decompressed = []

    for i in range(0, len(to_decompress), N):
        try:
            decompressed.append(dictionary[int(to_decompress[i:(i + N)], 2)])
        except IndexError:
            k = 1
            exit()
    if k == 0:
        file.write(''.join(decompressed))
