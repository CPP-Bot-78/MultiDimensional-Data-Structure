from lsh.lsh_static import one_hot_enc, backet_creator, jaccard, shingle, preprocess_data, vocab, log_lsh
import random


def minhash(shingles, hashes=50):
    """
    :param shingles:
    :param hashes:
    :return:
    """
    max_hash = 2 ** 32 - 1  # hash of 32 bits
    modulo = 2 ** 32

    funcs = []
    for _ in range(hashes):
        a, b = random.randint(0, max_hash), random.randint(0, max_hash)
        func = lambda x, y=a, z=b: (a * hash(x) + b) % modulo
        funcs.append(func)

    sign_x = [min([f(shingle) for shingle in shingles]) for f in funcs]

    return sign_x


def lsh(query, threshold):
    """ LSH algorithm
    :parameter list query: the query we are shingling
    :parameter threshold : the minimum threshold
    :return: List of pairs scientists with similarity in education above the threshold
    :rtype: list
    """
    # education_texts = [el['Surname'] for el in query]
    education_texts = [element[3] for element in query]
    education_texts = preprocess_data(education_texts)

    # Convert education data to shingles and calculate signatures
    shingles = [shingle(education) for education in education_texts]
    # one_hot_encoded_data, vocabulary = one_hot_encoding(shingles)
    # signatures = [minhash(s) for s in vocabulary]
    vocabulary = vocab(shingles)
    signatures = [minhash(one_hot_enc(s, vocabulary)) for s in shingles]

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
            # print(f'Found {[query[i], query[j]]}')  # DEBUG
            final_pairs.append([query[i], query[j]])
    # log_lsh(final_pairs, threshold, 'LSH_log.txt')
    return final_pairs
