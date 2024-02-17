import os
import string
from random import randint, uniform, sample
from lsh.lsh import lsh
from range_tree.Range_tree import build_range_tree, query_range_tree_by_ranges
from octree.octree import build_octree, query_octree
from kdtree.kdtree import build_kdtree, query_kdtree
from r_tree.r_tree import create_rtree, query_rtree_by_range
from time import time
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def create_new_demo(filename: str, count: int) -> str:
    """
     Δημιουργεί ένα νέο αρχείο με αποτελέσματα. Αν ήδη υπάρχει αρχείο με το ίδιο όνομα,
     μετονομάζει το νέο αρχείο προσθέτοντάς του έναν αριθμό στο επίθεμα
    :param filename: To όνομα του αρχείου που θέλουμε να εισάγουμε
    :param count: Ο αριθμός που θα προστεθεί στο τέλος αν ήδη υπάρχει αρχείο με όνομα ίσο με filename.
    Αυξάνεται σε κάθε επανάληψη μέχρι και το 50 (για εξοικονόμηση χώρου και ασφάλεια από infinite recursions)
    :return: To όνομα του νέου αρχείου
    :rtype: str
    """
    filename, extension = os.path.splitext(filename)
    count += 1
    # αφαιρούμε ήδη υπάρχον νούμερα για να μην πάμε πχ από file1 σε file12 σε file123 κλπ
    while filename[-1].isdigit():
        filename = filename[:-1]
    new_filename = f"{filename}{count}{extension}"  # προσθέτουμε το count στο τέλος του ονόματος
    if count == 50:
        return f"{filename}_50{extension}"
    if os.path.exists(new_filename):
        # αν υπάρχει ήδη ξανατρέχουμε με αυξημένο count κατά 1
        return create_new_demo(new_filename, count)
    else:
        return new_filename


def save_experiment(trees: list, results: list, test: list, lsh_results: list, build_times: list, query_times: list):
    """
    Σώζει τα αποτελέσματα του test στον φάκελο testing
    :param list trees: Η λίστα με τα δέντρα που ελέγχθηκαν. Περιέχει αντικείμενα
    :param list results: Λίστα που περιέχει τα αποτελέσματα(λίστες) από κάθε δέντρο
    :param list test: To Test Set ώστε να ξέρουμε πως προέκυψαν τα αποτελέσματα.
    :param list lsh_results: Λίστα που περιέχει το πλήθος των ζεύγων επιστημόνων με όμοια εκπαίδευση
    :param list build_times: Λίστα που περιέχει τους χρόνους κατασκευής των δέντρων
    :param list query_times: Λίστα που περιέχει τους χρόνους αναζήτησης των δέντρων
    :return: Nothing
    :rtype: None
    """
    # Το dir που δημιουργηθεί ο φάκελος αν δεν υπάρχει ήδη
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'results'
    FOLDERNAME = os.path.join(script_directory, FOLDERNAME)
    if not os.path.exists(FOLDERNAME):
        folder_path = os.path.join(script_directory, FOLDERNAME)
        os.makedirs(folder_path)
    os.chdir(FOLDERNAME)
    if os.path.exists('results.txt'):
        # Δημιουργεί ένα αρχείο με το ίδιο όνομα αλλά με ένα αριθμό πχ test2.
        # Όσο υπάρχουν αρχεία με το ίδιο όνομα θα δοκιμάζει με αυξημένο κατά 1 count, μέχρι να φτάσει στο 50
        demo_name = create_new_demo('results.txt', 1)
    else:
        # Δεν υπάρχει ήδη άρα θα μείνει ως έχει
        demo_name = 'results.txt'
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
            file.write(f"Totally found {len(tree_results)} with {lsh_res} pair/pairs of them with similar Education\n")
            if lsh_res > 0 and len(tree_results) != 0:
                if lsh_res > len(results):
                    '''pc = (lsh_res / len(results))
                    sq_root = sqrt(lsh_res)
                    pc = (pc / sq_root) * 10'''
                    pc = fix_pc(lsh_res, len(tree_results))
                    file.write(f'Similarity percentage is approximate: {pc:.2f} %\n')
                else:
                    file.write(f"Similarity percentage is: {(lsh_res / len(tree_results)) * 100:.2f} %\n")
            file.write(
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
        char_range = ['a', 'w']  # για αποφυγή λαθών
    test_set = [
        char_range,  # characters list
        randint(1, 20),  # Min Awards
        # f'{randint(1, 20)}-{randint(1, 10)*(randint(100, 1000))}',
        [randint(1, 20), randint(1, 10) * (randint(100, 1000))],  # DBLP Range
        # uniform(0.01, 1.0)  # Similarity Threshold
        uniform(0.4, 0.9)  # Below 0.4 it's no use
    ]
    return test_set


def auto_testing(trees_num: int, test: list):
    """
    Δημιουργεί τα δέντρα και κάνει αναζήτηση σε αυτά. Στο τέλος δημιουργεί ένα txt με τα αποτελέσματα
    :param int trees_num: Πλήθος των δέντρων για τα οποία θα γίνει το test
    :param list test: Το Test set
    :return: Λίστες με τους χρόνους δημιουργίας και αναζήτησης των δέντρων
    :rtype: list, list
    """
    # Λίστες για τα αποτελέσματα και τα δέντρα. Οι λίστες θα είναι ευθυγραμμισμένες ώστε να έχουν κοινό index
    TREES = []
    RESULTS = []
    LSH_RESULTS = []
    BUILD_TIMES = []
    QUERY_TIMES = []  # [[], [], [], []]
    # Οι συναρτήσεις δημιουργίας και αναζήτησης των δέντρων.
    # Είναι ευθυγραμμισμένες ώστε με το ίδιο index να παίρνουμε το ίδιο αποτέλεσμα
    BUILD_FUNCS = [create_rtree, build_octree, build_kdtree, build_range_tree]
    QUERY_FUNCS = [query_rtree_by_range, query_octree, query_kdtree, query_range_tree_by_ranges]

    for i in range(trees_num):  # χρησιμοποιούμε το index που είναι κοινό στους 2 πίνακες
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
        threshold = test[3]
        similar_science = lsh(results, test[3])
        query_finish = time() - query_start
        QUERY_TIMES.append(query_finish)
        RESULTS.append(results)
        # Επιπλέον, τυπώνονται στο terminal συνοπτικά αποτελέσματα
        print(tree.__str__())
        print(f"Construction Time: {build_finish} seconds\n")
        print(f"Range Query Time: {query_finish} seconds\n")
        print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]}'
              f' and DBLP from {test[2][0]} to {test[2][1]}')
        # Τυπώνονται τα αποτελέσματα του lsh των αποτελεσμάτων
        # Αν δε βρει τίποτα το μειώνει στο μισό και ξαναδοκιμάζει
        # Χρησιμοποιήθηκε πιο πολύ στην αξιολόγηση του LSH κατά το Debugging.
        # Επειδή καθυστερεί πολύ τον κώδικα το αφαιρούμε
        '''
        while len(similar_science) == 0 and (threshold - 0.1) > 0:  # threshold - 0.1 για να αποφευχθεί infinite loop
            print(f'No similar for {threshold * 100:.2f} %')
            threshold = threshold / 2
            similar_science = lsh(results, threshold)
        # print(similar_science)  # DEBUG
        print(f'For similarity above: {threshold * 100:.2f} % the results are: {len(similar_science)}')
        if threshold <= 0:
            print(f'No similar for {test[3] * 100:.2f} %')
        '''
        print(f'For similarity above: {threshold * 100:.2f} % we found: {len(similar_science)} similar pair/pairs.')
        if len(similar_science) != 0 and len(results) != 0:
            if len(similar_science) > len(results):
                '''pc = (len(similar_science) / len(results))
                sq_root = sqrt((len(similar_science)))
                pc = (pc / sq_root) * 1000'''
                pc = fix_pc(len(similar_science), len(results))
                print(f'Similarity percentage is approximate: {pc:.2f} %')
            else:
                print(f'Similarity percentage is: {(len(similar_science) / len(results)) * 100:.2f} %')
        print()
        print((lambda: "-" * 50)())
        LSH_RESULTS.append(len(similar_science))
    save_experiment(TREES, RESULTS, test, LSH_RESULTS, BUILD_TIMES, QUERY_TIMES)  # Αποθήκευση των αποτελεσμάτων
    return BUILD_TIMES, QUERY_TIMES


def fix_pc(lsh_res: int, query_res: int):
    pc = (lsh_res / query_res)
    sq_root = sqrt(lsh_res)
    pc = (pc / sq_root) * 1000
    return pc


def plot_results(build_time: list, query_time: list):
    """
     Υπολογίζει τους μέσους χρόνους της κατασκευής και αναζήτησης των δέντρων και δημιουργεί
     για αυτές 2 γραφικές παραστάσεις
    :param build_time: Η λίστα με τους χρόνους κατασκευής των 4ων δέντρων. Περιέχει λίστες μεγέθους 4
    :param query_time: Η λίστα με τους χρόνους αναζήτησης των 4ων δέντρων. Περιέχει λίστες μεγέθους 4
    :return: Nothing
    :rtype: None
    """
    trees = ["R Tree", "Octree", "KD Tree", "Range Tree"]
    trees_total_avg_build = []
    trees_total_avg_query = []
    for i in range(len(trees)):
        tree_avg_build = []
        trees_avg_query = []
        for j in range(len(build_time)):  # ίδιο index
            # σε κάθε υπο-λίστα των χρόνων, θέλω πχ το index 0 που είναι του rtree
            tree_avg_build.append(build_time[j][i])
            trees_avg_query.append(query_time[j][i])
        trees_total_avg_build.append(np.average(tree_avg_build))  # προσθέτω το average ime του κάθε δέντρου
        trees_total_avg_query.append(np.average(trees_avg_query))

    plt.figure()
    plt.bar(trees, trees_total_avg_build)
    plt.xlabel('Data Structure')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Average Execution Build Time for each Data Structure')
    plt.xticks(trees)
    plt.show()

    plt.figure()
    plt.bar(trees, trees_total_avg_query)
    plt.xlabel('Data Structure')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Average Execution Query + LSH Time for each Data Structure')
    plt.xticks(trees)
    plt.show()


def tree_testing(iterations: int = 20, test_set=None):
    """
     Πραγματοποιεί δοκιμές στα δέντρα ανάλογα με τον αριθμό επαναλήψεων που επιλέγει ο χρήστης.
     Η δοκιμή περιλαμβάνει κατασκευή και αναζήτηση σε συνδυασμό με εφαρμογή του LSH στα αποτελέσματα
     ώστε να εξαχθεί το ποσό όμοιων αποτελεσμάτων
    :param iterations: Ο αριθμός των ελέγχων που θα πραγματοποιηθούν
    :param list test_set: Λίστα με τα δεδομένα που θα γίνει η αναζήτηση στο δέντρο
    :return: Nothing
    :rtype: None
    """
    if test_set is None:
        test_set = get_test_set()
    if iterations < 1:  # Αποφυγή errors
        iterations = 1
    # Λίστες για τους χρόνους αναζήτησης και κατασκευής των δέντρων
    average_build_time = []
    average_query_time = []
    for i in range(iterations):
        # Πραγματοποιείται ένας έλεγχος
        b_time, q_time = auto_testing(4, test_set)
        test_set = get_test_set()  # Ανανεώνει το test_set αν χρειαστούν πολλές επαναλήψεις
        average_build_time.append(b_time)
        average_query_time.append(q_time)
    plot_results(average_build_time, average_query_time)
