import os
import string
from random import randint, uniform, sample
from lsh.lsh import lsh
from range_tree.Range_tree import build_range_tree, query_range_tree_by_ranges
from octree.octree import build_octree, query_octree
from kdtree.kdtree import build_kdtree, query_kdtree
from r_tree.r_tree import create_rtree, query_rtree_by_range
from demo import create_new_demo
from time import time

# Οι συναρτήσεις δημιουργίας και αναζήτησης των δέντρων.
# Είναι ευθυγραμμισμένες ώστε με το ίδιο index να παίρνουμε το ίδιο αποτέλεσμα
BUILD_FUNCS = [create_rtree, build_octree, build_kdtree, build_range_tree]
QUERY_FUNCS = [query_rtree_by_range, query_octree, query_kdtree, query_range_tree_by_ranges]


def save_experiment(trees: list, results: list, test: list, lsh_results: list, build_times: list, query_times: list):
    """
    Σώζει τα αποτελέσματα του test στον φάκελο testing
    :param list trees: Η λίστα με τα δέντρα που ελέγχθηκαν. Περιέχει αντικείμενα
    :param list results: Λίστα που περιέχει τα αποτελέσματα(λίστες) από κάθε δέντρο
    :param list test: To Test Set ώστε να ξέρουμε πως προέκυψαν τα αποτελέσματα.
    :param list lsh_results: Λίστα που περιέχει το πλήθος των ζεύγων επιστημόνων με όμοια εκπαίδευση
    :param list build_time: Λίστα που περιέχει τους χρόνους κατασκευής των δέντρων
    :param list query_time: Λίστα που περιέχει τους χρόνους αναζήτησης των δέντρων
    :return: Nothing
    :rtype: None
    """
    # Το dir που δημιουργηθεί ο φάκελος αν δεν υπάρχει ήδη
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'testing'
    FOLDERNAME = os.path.join(script_directory, FOLDERNAME)
    if not os.path.exists(FOLDERNAME):
        folder_path = os.path.join(script_directory, FOLDERNAME)
        os.makedirs(folder_path)
    os.chdir(FOLDERNAME)
    if os.path.exists('test.txt'):
        # Δημιουργεί ένα αρχείο με το ίδιο όνομα αλλά με ένα αριθμό πχ test2.
        # Όσο υπάρχουν αρχεία με το ίδιο όνομα θα δοκιμάζει με αυξημένο κατά 1 count, μέχρι να φτάσει στο 50
        demo_name = create_new_demo('test.txt', 1)
    else:
        # Δεν υπάρχει ήδη άρα θα μείνει ως έχει
        demo_name = 'test.txt'
    # Δημιουργούμε το αρχείο. Δημιουργείται εδώ ώστε στο for loop μετά να γίνεται append,
    # ώστε να κάθε αρχείο να έχει και τα 4 δέντρα
    with open(demo_name, 'w') as f:
        f.write("")
    # Επαναλαμβάνουμε για κάθε δέντρο
    for tree in trees:
        # Αντιστοίχηση του αποτελέσματος με index του αντικειμένου.
        tree_results = results[trees.index(tree)]
        lsh_res = lsh_results[trees.index(tree)]
        build_time = build_times[trees.index(tree)]
        query_time = query_times[trees.index(tree)]
        with open(demo_name, 'a', encoding='utf-8') as file:
            file.write(f"Results for {tree.__str__()}:\n")
            file.write(f"Construction Time: {build_time} seconds\n")
            file.write(f"Range Query Time: {query_time} seconds\n")
            file.write(
                f"Totally found {len(tree_results)} with {lsh_res} pair/pairs of them with similar Education\n"
                f"Given values were: Surname: {test[0]}, "
                f"min Awards: {test[1]}, "
                f"DBLP: {test[2]}, "
                f"Similarity: {test[3]:.2f}\n")
            file.write("Surname: , #Awards: , #DBLP: , Education:\n")
            for item in tree_results:
                if len(tree_results) != 0:
                    file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
            end_str = '\n' + ('-' * 10) + ('\n' * 2)
            file.write(end_str)


def get_test_set():
    """
    Ετοιμάζει ενα τυχαίο set για τη δοκιμή των δέντρων.
    :return: Λίστα που περιέχει [λίστα με 2 τυχαίους χαρακτήρες με αλφαβητική σειρά], τυχαίο ακέραιο για τα βραβεία,
    [λίστα με 2 ακεραίους για το DBLP από τον μικρότερο στον μεγαλύτερο], τυχαίο float για το lsh μεταξύ 0.4 και 0.9.

    :rtype: list
    """
    characters = string.ascii_lowercase[:24]
    num_samples = randint(1, len(characters))
    random_characters = sample(characters, num_samples)
    random_characters.sort()
    num_indices = min(2, len(random_characters))
    chars = sample(range(len(random_characters)), num_indices)
    selected_characters = [random_characters[i] for i in chars]
    char_range = sorted(selected_characters)
    if len(char_range) < 2:
        char_range = ['a', 'w']
    test_set = [
        char_range,  # characters list
        randint(1, 20),  # Min Awards
        # f'{randint(1, 20)}-{randint(1, 10)*(randint(100, 1000))}',
        [randint(1, 20), randint(1, 10) * (randint(100, 1000))],  # DBLP Range
        # uniform(0.01, 1.0)  # Similarity Threshold
        uniform(0.4, 0.9)  # Below 0.4 it's no use
    ]
    return test_set


def auto_testing(trees: list, test: list):
    """
    Δημιουργεί τα δέντρα και κάνει αναζήτηση σε αυτά. Στο τέλος δημιουργεί ένα txt με τα αποτελέσματα
    :param list trees: Λίστα με τις συναρτήσεις δημιουργίας των δέντρων. Χρειαζόμαστε το index της.
    :param list test: Το Test set
    :return: Nothing
    :rtype: None
    """
    # Λίστες για τα αποτελέσματα και τα δέντρα. Οι λίστες θα είναι ευθυγραμμισμένες ώστε να έχουν κοινό index
    TREES = []
    RESULTS = []
    LSH_RESULTS = []
    BUILD_TIMES = []
    QUERY_TIMES = []  # [[], [], [], []]
    for i in range(len(trees)):  # χρησιμοποιούμε το index που είναι κοινό στους 2 πίνακες
        build_start = time()
        try:
            tree = BUILD_FUNCS[i](test[1])  # Επειδή το KD Tree χρειάζεται τα awards στην κατασκευή
        except Exception:
            tree = BUILD_FUNCS[i]()  # για τα υπόλοιπα δέντρα
        build_finish = time() - build_start
        BUILD_TIMES.append(build_finish)
        # Αποθήκευση του δέντρου και των αποτελεσμάτων του
        TREES.append(tree)
        query_start = time()
        results = QUERY_FUNCS[i](tree, test[0], test[1], test[2])
        query_finish = time() - query_start
        QUERY_TIMES.append(query_finish)
        RESULTS.append(results)
        # Επιπλέον, τυπώνονται στο terminal συνοπτικά αποτελέσματα
        print(tree.__str__())
        print(f"Construction Time: {build_finish} seconds\n")
        print(f"Range Query Time: {query_finish} seconds\n")
        print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]}'
              f' and DBLP from {test[2][0]} to {test[2][1]}')
        threshold = test[3]
        similar_science = lsh(results, test[3])
        # Τυπώνονται τα αποτελέσματα του lsh των αποτελεσμάτων
        # Αν δε βρει τίποτα το μειώνει στο μισό και ξαναδοκιμάζει
        while len(similar_science) == 0 and (threshold - 0.1) > 0:  # threshold - 0.1 για να αποφευχθεί infinite loop
            print(f'No similar for {threshold * 100:.2f} %')
            threshold = threshold / 2
            similar_science = lsh(results, threshold)
        # print(similar_science)  # DEBUG
        print(f'For similarity above: {threshold * 100:.2f} % the results are: {len(similar_science)}')
        if threshold <= 0:
            print(f'No similar for {test[3] * 100:.2f} %')
        print()
        print((lambda: "-" * 50)())
        LSH_RESULTS.append(len(similar_science))
    save_experiment(TREES, RESULTS, test, LSH_RESULTS, BUILD_TIMES, QUERY_TIMES)  # Αποθήκευση των αποτελεσμάτων


if __name__ == '__main__':
    for i in range(100):
        auto_testing(BUILD_FUNCS, get_test_set())
