import math


# funkcja konwertujaca wartosc decymalna na binarna dodajac przy tym ew. zera wiodace
def to_binary(dec_value, bits_count):
    return format(dec_value, 'b').zfill(bits_count)


# odczytujemy wygenerowany plik z tekstem do kompresji
with open("do_kompresji.txt", "r") as file:
    text = file.read()

    print('Tekst do kompresji: ' + text + '\n')

# posortowana lista zawierajaca wypisany kazdy rodzaj znaku wystepujacego w tekscie
char_types_summary_list = sorted(list(set(text)))
print('Slownik: ' + ''.join(char_types_summary_list) + '\n')

# dlugosc tekstu przed kompresja
text_len = len(text)
print('Dlugosc tekstu przed kompresja: ' + str(text_len))

# ilosc typow znakow w tekscie
char_types_count = len(char_types_summary_list)
print('Unikalnych liter: ' + str(char_types_count))

# obliczenie minimalnej ilosci bitow potrzebnej na zakodowanie jednego znaku w tekscie
N = math.ceil(math.log2(char_types_count))
print('Liczba bitow na znak: ' + str(N))

# obliczenie ilosci nadmiarowych bitow, a konkretniej 1
R = (8 - (3 + text_len * N) % 8) % 8
print('Liczba nadmiarowych 1: ' + str(R) + '\n')

# tworzymy plik binarny ze skompresowanym tekstem
with open("skompresowany.txt", "wb") as compressed:

    # inicjalizacja pustej tablicy bajtów
    tab_of_b = bytearray()

    # dodanie do tablicy ilosci typow znakow w tekscie przed jego kompresja
    tab_of_b.append(char_types_count)

    # dodanie do tablicy elementow z listy zawierajacej wypisany kazdy rodzaj znaku wystepujacego w tekscie
    for char_type in char_types_summary_list:
        tab_of_b.append(ord(char_type))

    # inicjalizacja zmiennej przechowujacej nasz tekst w postaci ciagu 0 i 1
    binary_text = ""

    # dodajemy 3 bity, ktorych wartosc informuje nas o tym ile mamy dodac jedynek na koncu zakodowanego tekstu
    binary_text += to_binary(R, 3)

    # zamieniamy tekst do kompresji na ciag zer i jedynek
    for char in text:
        binary_text += to_binary(char_types_summary_list.index(char), N)

    # dodajemy nadmiarowe jedynki na koniec zakodowanego tekstu
    binary_text += '1' * R

    # wstawianie spacji co 8 znaków
    binary_text_spaced = " ".join(binary_text[i:i + 8] for i in range(0, len(binary_text), 8))
    print(binary_text_spaced + '\n')

    # inicjalizacja listy znakow
    list_of_chr = []

    # konwertujemy każde 8 bitow na znak ASCII
    for i in range(0, len(binary_text), 8):
        sign = chr(int(binary_text[i:(i + 8)], 2))

        print(ord(sign), end=" ")

        list_of_chr.append(sign)

        tab_of_b.append(ord(sign))

    print('\n\nSkompresowany tekst: ' + ''.join(char_types_summary_list) + ''.join(list_of_chr))
    print('Dlugosc tekstu po kompresji: ' + str(len(list_of_chr)))

    # zapisujemy do pliku nasz skompresowany tekst
    compressed.write(tab_of_b)
