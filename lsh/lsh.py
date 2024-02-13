from lsh import lsh_static
# from static import shingle, jaccard
import random
import pandas as pd
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
df = pd.read_csv(CSV_PATH)


def shingle(word, k=2):
    """:parameter str word: the text we are shingling
    :parameter int k: the number of 'digits' we are shingling"""
    shingle_set = []
    for i in range(len(word) - k + 1):
        shingle_set.append(word[i:i + k])
    return set(shingle_set)


def jaccard(s1, s2):
    intersect_size = len(s1.intersection(s2))
    union_size = len(s1.union(s2))
    # print(f"{intersect_size/union_size} this is the score")
    return intersect_size / union_size


def func_hash(a, b, modulo):
    return lambda x: (a * x + b) % modulo


def minhash(shingles, hashes=50):
    max_hash = 2 ** 32 - 1  # hash of 32 bits
    modulo = 2 ** 32

    funcs = []
    for _ in range(hashes):
        a, b = random.randint(0, max_hash), random.randint(0, max_hash)
        func = lambda x, y=a, z=b: (a * hash(x) + b) % modulo
        funcs.append(func)

    sign_x = [min([f(shingle) for shingle in shingles]) for f in funcs]

    return sign_x


def backet_creator(sign, bands, rows):
    buckets = []
    for band in range(bands):
        start = band * rows
        end = (band + 1) * rows
        buckets.append(hash(tuple(sign[start:end])))
    return buckets


def lsh(query, threshold):
    """
    :parameter list query: the query we are shingling
    :parameter threshold : the threshold we want to find"""
    # Extract education data from the query (assuming it's stored in Node objects)
    education_texts = [dict_el['surname'] for dict_el in query]

    # Convert education data to shingles and calculate signatures
    shingles = [shingle(education) for education in education_texts]
    signatures = [minhash(s) for s in shingles]

    bands = 10
    rows = 10
    buckets = [backet_creator(sign, bands, rows) for sign in signatures]

    pairs = set()

    for i, buckets1 in enumerate(buckets):
        for j, buckets2 in enumerate(buckets):
            if i != j and any(b1 == b2 for b1, b2 in zip(buckets1, buckets2)):
                if i < j:
                    pairs.add((i, j))
                else:
                    pairs.add((j, i))

    final_pairs = []
    for i, j in pairs:
        similarity = jaccard(shingles[i], shingles[j])
        if similarity >= threshold:
            final_pairs.append((query[i], query[j]))

    return final_pairs
