def vocab(kshingle):
    vocabulary = [kshingle]
    return vocabulary


def one_hot_enc(kshingle, vocabulary):
    one_hot = [1 if x in kshingle else 0 for x in vocabulary]
    return one_hot


def shingle(word, k=2):
    """ K Shingling Hash Table
    :parameter str word: the text we are shingling
    :parameter int k: the number of 'digits' we are shingling"""
    shingle_set = []
    for i in range(len(word) - k + 1):
        shingle_set.append(word[i:i + k])
    return set(shingle_set)


def jaccard(s1, s2):
    """ Jaccard Probability
    :parameter set s1: the 1st set we are shingling
    :parameter set s2: the 2nd set we are shingling
    :return float: Jaccard Probability
    :rtype: float"""
    intersect_size = len(s1.intersection(s2))
    union_size = len(s1.union(s2))
    # print(f"{intersect_size/union_size} this is the score")
    return intersect_size / union_size


def func_hash(a, b, modulo):
    """
    :param a:
    :param b:
    :param modulo:
    :return:
    """
    return lambda x: (a * x + b) % modulo


def backet_creator(sign, bands, rows):
    """
    :param sign:
    :param bands:
    :param rows:
    :return:
    """
    buckets = []
    for band in range(bands):
        start = band * rows
        end = (band + 1) * rows
        buckets.append(hash(tuple(sign[start:end])))
    return buckets

