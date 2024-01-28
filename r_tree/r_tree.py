import pandas as pd
from rtree import index
from auxiliary import letter_normalization

class RTree:
    def __init__(tree):
        tree.index = index.Index()  # Δημιουργία ενός R-tree index
        tree.dataList = []  # Λίστα για αποθήκευση των δεδομένων

    def insert(tree, itemId, item, x, y, z):
        tree.idx.insert(itemId, (x, y, z, x, y, z))
        tree.dataList.append(item)

    def search(tree, qbbox):
        return list(tree.idx.intersection(qbbox))


def build_rtree():
    df = pd.read_csv("./scientists_data.csv")
    rtree = RTree()  # Δημιουργία ενός νέου R-tree

    # Για κάθε εγγραφή του dataframe, υπολογίζουμε τις συντεταγμένες (x, y,z) βάσει της αριθμητική τιμής του πρώτου γράμματος του επωνύμου του αριθμού των βραβείων και του αριθμού των σημοσιεύεσεων στο DBLP Record αντίστοιχα, και εισάγουμε το στοιχείο στο R-tree.
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['surname'][0])
        y = df.iloc[i]['awards']
        z = df.iloc[i]['BDLP_Record']
        data = (df.iloc[i]['surname'], df.iloc[i]['awards'], df.iloc[i]['BDLP_Record'])
        rtree.insert(i, data, x, y, z)  # Εισαγωγή του στοιχείου στο R-tree

    return rtree


def query_rtree(rtree, minLetter, maxLetter, numAwards, minDLP_Record, maxDLP_Record):
    # Υπολογισμός των αριθμητικών τιμών του ελάχιστου και του μέγιστου γράμματος

    minLetter = letter_normalization(minLetter)
    maxLetter = letter_normalization(maxLetter)

    qbbox = (minLetter, minDLP_Record, numAwards, maxDLP_Record, maxLetter, float('inf'))
    matches = rtree.search(qbbox)  # Αναζήτηση στο R-tree με βάση το δοθέν query_bbox

    queryResults = []
    # Ανάκτηση των δεδομένων από τα αποτελέσματα της αναζήτησης
    for match in matches:
        surname, awards, BDLP_Record = rtree.data_list[match]
        queryResults.append({"surname": surname, "awards": awards, "BDLP_Record": BDLP_Record})

    return queryResults