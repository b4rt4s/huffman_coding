import math


# funkcja konwertujaca wartosc decymalna na binarna dodajac przy tym ew. zera wiodace
def to_binary(dec_value, bits_count):
    return format(dec_value, 'b').zfill(bits_count)


# odczytujemy wygenerowany plik z tekstem do kompresji
with open("do_kompresji.txt", "r") as file:
    text = file.read()

# posortowana lista zawierajaca wypisany kazdy rodzaj znaku wystepujacego w tekscie
char_types_summary_list = sorted(list(set(text)))
print('Slownik: ' + ''.join(char_types_summary_list))

# ilosc typow znakow w tekscie
X = len(char_types_summary_list)
print('X: ' + str(X))

# obliczenie minimalnej ilosci bitow potrzebnej na zakodowanie jednego znaku w tekscie
N = math.ceil(math.log2(X))
print('N: ' + str(N))

# obliczenie ilosci nadmiarowych bitow, a konkretniej 1
R = (8 - (3 + len(text) * N) % 8) % 8
print('R: ' + str(R))

# dlugosc tekstu przed kompresja
print('Dlugosc tekstu: ' + str(len(text)))

# tworzymy plik binarny ze skompresowanym tekstem
with open("skompresowany.txt", "wb") as compressed_end_encrypted:

    # ---------------
    #    KOMPRESJA
    # ---------------

    # inicjalizacja pustej listy bajtów
    compressed_text = bytearray()

    # dodanie do listy ilosci typow znakow w tekscie przed jego kompresja
    compressed_text.append(X)

    # dodanie do listy elementow z listy zawierajacej wypisany kazdy rodzaj znaku wystepujacego w tekscie
    compressed_text += bytes([ord(char_type) for char_type in char_types_summary_list])

    # inicjalizacja zmiennej przechowujacej nasz tekst w postaci ciagu 0 i 1
    binary_text = ""

    # dodajemy 3 bity, ktorych wartosc informuje nas o tym ile mamy dodac jedynek na koncu zakodowanego tekstu
    binary_text += to_binary(R, 3)

    # zamieniamy tekst do kompresji na ciag zer i jedynek
    binary_text += ''.join([to_binary(char_types_summary_list.index(char), N) for char in text])

    # dodajemy nadmiarowe jedynki na koniec zakodowanego tekstu
    binary_text += '1' * R

    list_of_chr = []

    # konwertujemy każde 8 bitow na znak ASCII
    for i in range(0, len(binary_text), 8):
        sign = chr(int(binary_text[i:(i + 8)], 2))

        list_of_chr.append(sign)

        compressed_text.append(ord(sign))

    print('Dlugosc tekstu po kompresji: ' + str(len(list_of_chr)))

    # ---------------
    #   SZYFROWANIE
    # ---------------

    # zainicjowanie rozszerzonej tablicy ASCII o zakresie znakow od 0 do 255
    tab_of_ascii_lists = [[col + row - 256 if col + row > 255 else col + row
                           for col in range(256)] for row in range(256)]

    key = input('Podaj klucz: ')

    # zabezpieczenie na wypadek nie podania klucza
    if len(key) == 0:
        print('Bez podania klucza kompresja jest niemozliwa!')
        exit()

    index = 0

    tab_encrypt = []

    # szyfrowanie skompresowanego tekstu
    for char in compressed_text:
        # decymalna wartość danego znaku klucza
        key_char = ord(key[index])

        # zapisanie do tablicy zaszyfrowanych znaków skompresowanego tekstu
        tab_encrypt.append(tab_of_ascii_lists[key_char][char])

        # resetowanie indeksu znaku w kluczu, gdyby byl on krotszy niz tekst do zaszyfrowania
        index = (index + 1) % len(key)

    # zapisujemy do pliku nasz skompresowany i zaszyfrowany tekst
    compressed_end_encrypted.write(bytes(tab_encrypt))
