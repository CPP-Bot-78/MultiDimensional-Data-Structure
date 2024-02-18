"""
Η λογική ενός τρισδιάστατου (3D) Range Tree είναι ότι για μία δοθείσα συλλογή από σημεία P,
κατασκευάζουμε αρχικά ένα BBST (Binary Balanced Search Tree) βασισμένο στις συντεταγμένες x
των σημείων. Έπειτα, κάθε κόμβος του αρχικού BBST, αποθηκεύει ένα δευτερεύον BBST, το οποίο
κατασκευάζεται από τα σημεία που έχουν την ίδια συντεταγμένη x με τον τρέχοντα κόμβο, αλλά
ταξινομημένα βάσει των συντεταγμένων y τους. Αντίστοιχα για τα σημεία z.
"""

import os
import pandas as pd
from range_tree import RangeTree3D as R3D
from range_tree.static import letter_normalization
import sys
from memory_profiler import profile


# Ετοιμάζουμε το dataframe για να φορτωθεί στο δέντρο
script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
df = pd.read_csv(CSV_PATH)


# @profile Remove comment for memory profiling
def build_range_tree():
    """
    Δημιουργεί κai επιστρέφει το range tree.
    :return: To 3D δέντρο με τα δεδομένα του dataframe
    :rtype: RangeTree3D
    """
    points = []
    # Για κάθε εγγραφή του dataframe, υπολογίζουμε τις συντεταγμένες (x, y, z)
    # βάσει της αριθμητικής τιμής του πρώτου γράμματος του επωνύμου, του
    # αριθμού των βραβείων και των εγγραφών DBLP, και εισάγουμε το σημείο στη λίστα points.
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['Surname'][0])
        y = df.iloc[i]['#Awards']
        z = df.iloc[i]['DBLP']
        points.append((x, y, z, i))

    range_tree = R3D.RangeTree3D(points)    # δημιουργία ενός νέου Range Tree για τα δοθέντα points
    return range_tree


# @profile
def query_range_tree(range_tree, min_letter, max_letter, num_awards, dblp_min, dblp_max):
    """ Πραγματοποιεί αναζήτηση στο Range Tree
    :param RangeTree3D range_tree: Το δέντρο περνάει ως αντικείμενο για να γίνει η αναζήτηση
    :param str min_letter: Το αρχικό του ονόματος όπου ξεκινά η αναζήτηση
    :param str max_letter: Το αρχικό του ονόματος όπου ολοκληρώνεται η αναζήτηση
    :param int num_awards: Ο ελάχιστος αριθμός βραβείων που πρέπει να έχει ώστε να συμπεριληφθεί στην αναζήτηση
    :param int dblp_min: Ο ελάχιστος αριθμός εγγραφών DBLP ώστε να συμπεριληφθεί στην αναζήτηση
    :param int dblp_max: Ο μέγιστος αριθμός εγγραφών DBLP ώστε να συμπεριληφθεί στην αναζήτηση
    :return: H λίστα με τα αποτελέσματα της αναζήτησης
    :rtype: list
    """
    # Υπολογισμός των αριθμητικών τιμών του ελάχιστου και του μέγιστου γράμματος
    min_letter = letter_normalization(min_letter)
    max_letter = letter_normalization(max_letter)

    # Ορισμός των διαστημάτων τόσο στις συντεταγμένες x, y, z πάνω στις οποίες θα γίνει η αναζήτηση
    x_range = (min_letter, max_letter)
    y_range = (num_awards, sys.maxsize)  # χρήση του maxsize μιας και μας ενδιαφέρει μόνο το ελάχιστο
    z_range = (dblp_min, dblp_max)
    query_results = []
    # Αποστολή ερωτήματος στο Range Tree και αποθήκευση των αποτελεσμάτων στη λίστα query_results
    range_tree.query(
        range_tree.root,
        x_range[0], x_range[1],
        y_range[0], y_range[1],
        z_range[0], z_range[1],
        query_results
    )

    final_results = []
    # Ανάκτηση των δεδομένων και αποθήκευσή τους σε λίστα
    for result in query_results:
        index = result[3]  # παίρνουμε το index από τα δεδομένα του Range Tree
        surname = df.iloc[index]['Surname']
        awards = df.iloc[index]['#Awards']
        education = df.iloc[index]['Education']
        dblp = df.iloc[index]['DBLP']
        final_results.append([surname, awards, dblp, education])
    # καθαρισμός από διπλότυπα και επιστροφή σορταρισμένης λίστας
    final_results = clean_results(final_results)
    return sorted(final_results, key=lambda x: x[0], reverse=False)


def clean_results(results):
    """ Καθαρισμός της λίστας από διπλότυπα
    :parameter list results: Η λίστα με τα αποτελέσματα. Περιέχει λίστες
    :return: Η λίστα χωρίς διπλότυπα
    :rtype list"""
    if len(results) == 0:
        return results
    unique_sc = []  # τα unique αποτελέσματα
    seen = []  # φυλάμε όσα ονόματα έχουμε ξαναδεί
    for item in results:
        name = item[0]
        if name not in seen:
            seen.append(name)
            unique_sc.append(item)
    return unique_sc


def query_range_tree_by_ranges(range_tree, surname_range, award, dblp_range):
    """ Πραγματοποιεί αναζήτηση στο Range Tree
    και έχει παρόμοια δομή με την αντίστοιχη συνάρτηση των άλλων δέντρων
    :param RangeTree3D range_tree: Το δέντρο περνάει ως αντικείμενο για να γίνει η αναζήτηση
    :param list surname_range: Λίστα με τα 2 αρχικά γράμματα
    :param int award: Ο ελάχιστος αριθμός βραβείων
    :param list dblp_range: Λίστα με το ελάχιστο και μέγιστο αριθμό των εγγραφών DBLP
    :return: H λίστα με τα αποτελέσματα της αναζήτησης
    :rtype: list
    """
    result_list = query_range_tree(
        range_tree,
        surname_range[0], surname_range[1],
        award,
        dblp_range[0], dblp_range[1],
    )
    return result_list
