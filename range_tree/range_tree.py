"""
Η λογική ενός τρισδιάστατου (3D) Range Tree είναι ότι για μία δοθείσα συλλογή από σημεία P,
κατασκευάζουμε αρχικά ένα BBST (Binary Balanced Search Tree) βασισμένο στις συντεταγμένες x
των σημείων. Έπειτα, κάθε κόμβος του αρχικού BBST, αποθηκεύει ένα δευτερεύον BBST, το οποίο
κατασκευάζεται από τα σημεία που έχουν την ίδια συντεταγμένη x με τον τρέχοντα κόμβο, αλλά
ταξινομημένα βάσει των συντεταγμένων y τους. Αντίστοιχα για τα σημεία z.
"""

import pandas as pd
from static import letter_normalization
from RangeTree3D import RangeTree3D


def build_range_tree():
    df = pd.read_csv("../computer_scientists_data.csv")
    points = []

    # Για κάθε εγγραφή του dataframe, υπολογίζουμε τις συντεταγμένες (x, y, z)
    # βάσει της αριθμητικής τιμής του πρώτου γράμματος του επωνύμου και του
    # αριθμού των βραβείων αντίστοιχα, και εισάγουμε το σημείο στη λίστα points.
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['Surname'][0])
        y = df.iloc[i]['#Awards']
        z = df.iloc[i]['DBLP']
        points.append((x, y, z, i))

    range_tree = RangeTree3D(points)    # δημιουργία ενός νέου Range Tree για τα δοθέντα points
    return range_tree


def query_range_tree(range_tree, min_letter, max_letter, num_awards):
    # Υπολογισμός των αριθμητικών τιμών του ελάχιστου και του μέγιστου γράμματος
    min_letter = letter_normalization(min_letter)
    max_letter = letter_normalization(max_letter)

    # Ορισμός των διαστημάτων τόσο στη συντεταγμένη x όσο και στη y, πάνω στα οποία θα γίνει η αναζήτηση
    x_range = (min_letter, max_letter)
    y_range = (num_awards, float('inf'))
    z_range = (min_letter, max_letter)
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
    df = pd.read_csv("./computer_scientists_data.csv")
    # Ανάκτηση των δεδομένων και αποθήκευσή τους σε λίστα
    for result in query_results:
        index = result[2]  # παίρνουμε το index από τα δεδομένα του Range Tree
        surname = df.iloc[index]['surname']
        awards = df.iloc[index]['awards']
        education = df.iloc[index]['education']
        final_results.append({"surname": surname, "awards": awards, "education": education})

    return final_results
