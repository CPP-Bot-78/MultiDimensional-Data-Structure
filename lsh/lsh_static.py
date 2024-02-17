import re
import nltk
from nltk.corpus import stopwords

if not nltk.download('stopwords', quiet=True):
    print('Downloading the stopwords corpus')
    nltk.download('stopwords')


def preprocess_data(data):
    """
    Καθαρίζει τα δεδομένα του 'education' από stopwords και κοινές λέξεις ώστε να δημιουργηθεί ένα vocabulary για το LSH
    :param list data: Λίστα με τα πεδία εκπαίδευσης. Περιέχει λίστες
    :return: Δεδομένα καθαρά κι έτοιμα για την επόμενη φάση του LSH
    :rtype: list
    """
    custom_stopwords = set(stopword.lower() for stopword in stopwords.words('english'))
    # Προσθέτουμε άλλες κοινές λέξεις για τα δεδομένα μας που οδηγούν το lsh σε λανθασμένα αποτελέσματα
    custom_stopwords.add('university')
    custom_stopwords.add('higher')
    custom_stopwords.add('education')
    custom_stopwords.add('institute')
    custom_stopwords.add('state')
    cleaned_data = []
    for document in data:
        cleaned_document = []
        try:
            # Τα δεδομένα της λίστας χωρίζονται
            for word in document.split():
                # Καθαρίζει τα δεδομένα μετατρέποντας πχ το 'University,' και το 'University]' σε 'University' σκέτο
                # Έτσι εξασφαλίζουμε ότι δε θα περάσουν λέξεις που θα επηρεάσουν αρνητικά τον LSH
                cleaned_word = re.sub(r'[\'\"\[\],.]', '', word.lower())
                if cleaned_word not in custom_stopwords:
                    cleaned_document.append(cleaned_word.lower())
            cleaned_data.append(' '.join(cleaned_document))
        except Exception as e:
            # Η λίστα περιέχει μόνο ένα στοιχείο και δε χωρίζεται
            for word in document:
                # log_lsh(f"[{e}] for {word}\n", 1, 'error.txt')  # DEBUG
                cleaned_word = re.sub(r'[\'\"\[\],.]', '', word.lower())
                if cleaned_word not in custom_stopwords:
                    cleaned_document.append(cleaned_word.lower())
            cleaned_data.append(' '.join(cleaned_document))
    return cleaned_data


def one_hot_enc(kshingle, vocabulary):
    """
    Μετατροπή των shingles σε one hot encoding με βάση το vocabulary
    :param set kshingle: Set με τα shingles
    :param vocabulary: To κοινό vocabulary
    :return: One-hot encoded shingle
    :rtype: list
    """
    one_hot = [1 if x in kshingle else 0 for x in vocabulary]
    return one_hot


def vocab(kshingles):
    """
    Δημιουργεί ενα κοινό vocabulary από όλα τα μοναδικά shingles.
    :param list kshingles: Λίστα με όλα τα shingles των δεδομένων
    :return: Vocabulary με όλα τα μοναδικά kshingles
    :rtype: set
    """
    vocabulary = set().union(*kshingles)
    return vocabulary


def shingle(word, k=2):
    """ K-Shingling Hash Table
    :param str word: Τα δεδομένα που κάνουμε shingling
    :param int k: το νούμερο των 'ψηφίων' που κάνουμε shingling"""
    shingle_set = []
    for i in range(len(word) - k + 1):
        # χωρίζεται σε υπο-λέξεις μεγέθους k
        shingle_set.append(word[i:i + k])
    # κρατάμε τις μοναδικές
    return set(shingle_set)


def jaccard(s1, s2):
    """ Μετρική Jaccard
    :parameter set s1: πρώτο set με shingles
    :parameter set s2: δεύτερο set με shingles
    :return float: Μετρική Jaccard των 2 sets
    :exception ZeroDivisionError: Όταν δεν υπάρχουν κοινά δεδομένα μεταξύ των set
    :rtype: float"""
    try:
        intersect_size = len(s1.intersection(s2))
        union_size = len(s1.union(s2))
        return intersect_size / union_size
    except ZeroDivisionError:
        return 0


'''def func_hash(a, b, modulo):
    """
    :param int a: random Number 1
    :param int b: random Number 2
    :param modulo: Hash Value of Input
    :return: Hash Value
    :rtype: int
    """
    return lambda x: (a * x + b) % modulo
'''


def bucket_creator(sign, bands, rows):
    """
    :param sign: MinHash signature
    :param int bands: Πλήθος των band που θα χωριστεί
    :param int rows: Πλήθος γραμμών του band
    :return: Η λίστα με τα buckets
    :rtype: list
    """
    buckets = []
    for band in range(bands):
        start = band * rows
        end = (band + 1) * rows
        buckets.append(hash(tuple(sign[start:end])))
    return buckets


def log_lsh(results_list: list, threshold: float, filename: str, exception: Exception = None):
    """
     Συνάρτηση που αποθηκεύει τα αποτελέσματα του lsh στο αρχείο με όνομα filename.
     Χρησιμοποιούταν για αξιολόγηση του lsh.
    :param list results_list: Η λίστα που θα αποθηκεύσουμε
    :param float threshold: lsh threshold
    :param str filename: Το όνομα του αρχείου που σώζονται τα δεδομένα
    :param Exception exception: Προαιρετικά αναγράφεται το exception που προκάλεσε logging
    :return: Nothing
    :rtype: None
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
