import unicodedata
from unicodedata import normalize


def letter_normalization(letter):
    letter = normalize('NFD', letter)
    filtered_letter = ''.join(c for c in letter if unicodedata.category(c) != 'Mn')
    return ord(filtered_letter.upper())-65
