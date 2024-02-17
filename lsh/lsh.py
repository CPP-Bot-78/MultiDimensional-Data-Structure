from lsh.lsh_static import one_hot_enc, bucket_creator, jaccard, shingle, preprocess_data, vocab, log_lsh
import random


def minhash(shingles, hashes=50):
    """
    Παράγει τα signatures
    :param list shingles: Ta one hot encoded shingles
    :param int hashes: Πλήθος των επαναλήψεων που θα γίνουν
    :return: Signatures για τα shingles
    :rtype: list
    """
    max_hash = 2 ** 32 - 1  # hash of 32 bits
    modulo = 2 ** 32

    funcs = []
    # Δημιουργία των hash functions
    for _ in range(hashes):
        a, b = random.randint(0, max_hash), random.randint(0, max_hash)
        func = lambda x, y=a, z=b: (a * hash(x) + b) % modulo
        funcs.append(func)
    # Αποθηκεύουμε το ελάχιστο των hashed shingles για κάθε συνάρτηση
    sign_x = [min([f(shingle) for shingle in shingles]) for f in funcs]

    return sign_x


def lsh(query, threshold):
    """ LSH algorithm
    :parameter list query: the query we are shingling
    :parameter threshold : the minimum threshold
    :return: List of pairs scientists with similarity in education above the threshold
    :rtype: list
    """
    # Ξεχωρίζουμε το πεδίο education από τα υπόλοιπα δεδομένα
    education_texts = [element[3] for element in query]
    # Καθαρίζουμε τα δεδομένα
    education_texts = preprocess_data(education_texts)

    # Βρίσκουμε τα shingles των λέξεων στα καθαρά δεδομένα
    shingles = [shingle(education) for education in education_texts]
    # Υπολογίζουμε το κοινό vocabulary όλων των shingles
    vocabulary = vocab(shingles)
    # Δημιουργούμε signatures για κάθε single. Τα shingles μετατρέπονται
    # πρώτα σε one hot encoded αναπαράσταση
    signatures = [minhash(one_hot_enc(s, vocabulary)) for s in shingles]

    # Διαστάσεις του bucket
    bands = 10
    rows = 10
    #
    buckets = [bucket_creator(sign, bands, rows) for sign in signatures]

    pairs = set()
    # Υπολογισμός candidate pairs
    for i, buckets1 in enumerate(buckets):
        for j, buckets2 in enumerate(buckets):
            if i != j and any(b1 == b2 for b1, b2 in zip(buckets1, buckets2)):
                if i < j:
                    pairs.add((i, j))
                else:
                    pairs.add((j, i))
    # Χρήση της μετρικής Jaccard για την επιλογή των τελικών ζευγαριών
    final_pairs = []
    for i, j in pairs:
        similarity = jaccard(shingles[i], shingles[j])
        if similarity >= threshold:
            # print(f'Found {[query[i], query[j]]}')  # DEBUG
            final_pairs.append([query[i], query[j]])
    # log_lsh(final_pairs, threshold, 'LSH_log.txt')  # DEBUG
    return final_pairs
