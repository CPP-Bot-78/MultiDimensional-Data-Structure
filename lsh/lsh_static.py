from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
if not nltk.download('stopwords', quiet=True):
    # Download the stopwords corpus
    nltk.download('stopwords')


def preprocess_data(data):
    custom_stopwords = set(stopword.lower() for stopword in stopwords.words('english'))
    custom_stopwords.add('university')
    custom_stopwords.add('institute')
    cleaned_data = [' '.join([word for word in document.split() if word.lower() not in custom_stopwords]) for document in data]
    return cleaned_data
'''
def preprocess_data(data):
    custom_stopwords = set(stopwords.words('english'))
    custom_stopwords.add('University')
    custom_stopwords.add('university')
    cleaned_data = [' '.join([word for word in document.split() if word not in custom_stopwords]) for document in data]
    return cleaned_data
'''

def one_hot_encoding(data):
    # Initialize a Count Vectorizer to convert text data to one-hot encoding
    vectorizer = CountVectorizer(binary=True)

    # Fit the vectorizer to the data and transform the data into one-hot encoded vectors
    one_hot_encoded_data = vectorizer.fit_transform(data)

    # Extract vocabulary from the vectorizer
    vocabulary = vectorizer.vocabulary_

    return one_hot_encoded_data, vocabulary


def vocab(kshingles):
    """
    :param list kshingles:
    :return: Vocabulary of all kshingles
    :rtype: set
    """
    vocabulary = set().union(*kshingles)
    return vocabulary


def one_hot_enc(kshingle, vocabulary):
    """
    :param set kshingle: Shingle sets
    :param vocabulary: The shared vocabulary
    :return: One-hot encoded shingle
    :rtype: list
    """
    one_hot = [1 if x in kshingle else 0 for x in vocabulary]
    return one_hot


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
    intersect_size = len(s1.intersection(s2))
    union_size = len(s1.union(s2))
    return intersect_size / union_size


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

