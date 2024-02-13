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

script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
df = pd.read_csv(CSV_PATH)
# test = 'computer_scientists_data1.csv'


# @profile
def build_range_tree():
    # df = pd.read_csv("../computer_scientists_data1.csv")
    points = []
    # Για κάθε εγγραφή του dataframe, υπολογίζουμε τις συντεταγμένες (x, y, z)
    # βάσει της αριθμητικής τιμής του πρώτου γράμματος του επωνύμου και του
    # αριθμού των βραβείων αντίστοιχα, και εισάγουμε το σημείο στη λίστα points.
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['Surname'][0])
        # x = df.iloc[i]['Surname'][0]
        y = df.iloc[i]['#Awards']
        z = df.iloc[i]['DBLP']
        points.append((x, y, z, i))

    range_tree = R3D.RangeTree3D(points)    # δημιουργία ενός νέου Range Tree για τα δοθέντα points
    return range_tree


# @profile
def query_range_tree(range_tree, min_letter, max_letter, num_awards, dblp_min, dblp_max):
    # Υπολογισμός των αριθμητικών τιμών του ελάχιστου και του μέγιστου γράμματος
    min_letter = letter_normalization(min_letter)
    max_letter = letter_normalization(max_letter)

    # Ορισμός των διαστημάτων τόσο στις συντεταγμένες x, y, z πάνω στις οποίες θα γίνει η αναζήτηση
    x_range = (min_letter, max_letter)
    y_range = (num_awards, sys.maxsize)
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
        # final_results.append({"surname": surname, "awards": awards, "education": education, "DBLP": dblp})
        final_results.append([surname, awards, dblp, education])
    final_results = clean_results(final_results)
    return sorted(final_results, key=lambda x: x[0], reverse=False)
    # return clean_results(final_results)


def clean_results(results):
    """
    :parameter list results: list of dictionaries
    :return: list of dictionaries
    :rtype list"""
    if len(results) == 0:
        return results
    unique_sc = []
    seen = []
    for item in results:
        # name = item.get('surname')
        name = item[0]
        if name not in seen:
            seen.append(name)
            unique_sc.append(item)
    return unique_sc


def query_range_tree_by_ranges(range_tree, surname_range, award, dblp_range):
    result_list = query_range_tree(
        range_tree,
        surname_range[0], surname_range[1],
        award,
        dblp_range[0], dblp_range[1],
    )
    return result_list
