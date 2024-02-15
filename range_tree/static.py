import unicodedata
from unicodedata import normalize


def letter_normalization(letter):
    """
    Μετατρέπει τα γράμματα σε αριθμητικές τιμές από 0 (Α) έως 25 (Z), ανεξαρτήτως αλφαβήτου(λατινικό, γερμανικό κλπ)
    :param str letter: To γράμμα που κανονικοποιούμε.
    :return: Η κανονικοποιημένη τιμή μεταξύ 0-25.
    :rtype: int
    """
    letter = normalize('NFD', letter)  # μετατρέπει το é σε e', το ó σε o' etc.
    # αφαιρεί τον 2ο χαρακτήρα πχ το ' από το e'
    filtered_letter = ''.join(c for c in letter if unicodedata.category(c) != 'Mn')
    # 65 είναι η ascii τιμή του κεφαλαίου A capital. 90 του κεφαλαίου Z
    return ord(filtered_letter.upper()) - 65
