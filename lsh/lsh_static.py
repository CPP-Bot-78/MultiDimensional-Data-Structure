import re
import nltk
from nltk.corpus import stopwords

if not nltk.download('stopwords', quiet=True):
    print('Downloading the stopwords corpus')
    nltk.download('stopwords')


def preprocess_data(data):
    """
    Cleans the education data from common stopwords and common words
    :param list data: Education data list
    :return: Education data without stopwords and common words
    :rtype: list
    """
    custom_stopwords = set(stopword.lower() for stopword in stopwords.words('english'))
    custom_stopwords.add('university')
    custom_stopwords.add('higher')
    custom_stopwords.add('education')
    custom_stopwords.add('institute')
    custom_stopwords.add('state')
    cleaned_data = []
    for document in data:
        cleaned_document = []
        try:
            for word in document.split():
                cleaned_word = re.sub(r'[\'\"\[\],.]', '', word.lower())
                if cleaned_word not in custom_stopwords:
                    cleaned_document.append(cleaned_word.lower())
            cleaned_data.append(' '.join(cleaned_document))
        except Exception as e:
            for word in document:
                # log_lsh(f"[{e}] for {word}\n", 1, 'error.txt')
                cleaned_word = re.sub(r'[\'\"\[\],.]', '', word.lower())
                if cleaned_word not in custom_stopwords:
                    cleaned_document.append(cleaned_word.lower())
            cleaned_data.append(' '.join(cleaned_document))
    return cleaned_data


def one_hot_enc(kshingle, vocabulary):
    """
    :param set kshingle: Shingle sets
    :param vocabulary: The shared vocabulary
    :return: One-hot encoded shingle
    :rtype: list
    """
    one_hot = [1 if x in kshingle else 0 for x in vocabulary]
    return one_hot


def vocab(kshingles):
    """
    :param list kshingles:
    :return: Vocabulary of all kshingles
    :rtype: set
    """
    vocabulary = set().union(*kshingles)
    return vocabulary


def shingle(word, k=2):
    """ K-Shingling Hash Table
    :parameter str word: the text we are shingling
    :parameter int k: the number of 'digits' we are shingling"""
    shingle_set = []
    for i in range(len(word) - k + 1):
        shingle_set.append(word[i:i + k])
    return set(shingle_set)


def jaccard(s1, s2):
    """ Jaccard Coefficient
    :parameter set s1: the 1st set of shingles
    :parameter set s2: the 2nd set of shingles
    :return float: Jaccard Coefficient of the 2 sets
    :rtype: float"""
    try:
        intersect_size = len(s1.intersection(s2))
        union_size = len(s1.union(s2))
        return intersect_size / union_size
    except ZeroDivisionError:
        return 0


def func_hash(a, b, modulo):
    """
    :param int a: random Number 1
    :param int b: random Number 2
    :param modulo: Hash Value of Input
    :return: Hash Value
    :rtype: int
    """
    return lambda x: (a * x + b) % modulo


def backet_creator(sign, bands, rows):
    """
    :param sign: MinHash signature
    :param int bands: Number of bands to divide into
    :param int rows: Number of rows in each band
    :return:
    """
    buckets = []
    for band in range(bands):
        start = band * rows
        end = (band + 1) * rows
        buckets.append(hash(tuple(sign[start:end])))
    return buckets


def log_lsh(results_list: list, threshold: float, filename: str, exception: Exception = None):
    """
    :param list results_list: The list of results we are logging
    :param float threshold: lsh threshold
    :param str filename: Filename to save the results to
    :param Exception exception: Optionally specify the exception that caused logging
    :return:
    """
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Results for {threshold * 100:.2f} %\n")
        if exception is not None:
            file.write((lambda: "=" * 50)())
            file.write(f'{exception}')
            file.write((lambda: "=" * 50)())
        for res in results_list:
            file.write(f'{res}')
        file.write('\n')

