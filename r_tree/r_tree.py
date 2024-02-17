import pandas as pd
import os
import sys
import unicodedata
from unicodedata import normalize
from rtree import index

#διάβασμα .csv αρχείου
script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
df = pd.read_csv(CSV_PATH)

#Κλάση του RTree, γίνεται χρήση του Index που περιέχει η βιβλιοθήκη rtree για την υλοποίηση των βασικών λειτουργιών του δέντρου
class RTree:
    #ορισμός τριών διαστάσεων
    def __init__(self):
        self.index3d = index.Index(properties=index.Property(dimension=3))
        self.dataList = []
    #μέθοδος που επιστρέφει το λεκτικό R Tree, για χρήση στο demo.py και testing.py για την εγγαραφή του .txt αρχείου αποτελεσμάτων
    def __str__(self):
        return "R Tree"
    #μέθοδος που εισάγει ένα νέο στοιχείο/φύλλο στο δέντρο βάση των συντεταγμένων του (x,y,z). Το itemId αναφέρεται στο
    #μοναδικό id που θα έχει το στοιχείο στο δέντρο και το item είναι λίστα που αποθηκεύει της πληροφορίες του στοιχείου 
    #όπως αναφέρονται στο csv αρχείο
    def insert(self, itemId, item, x, y, z):
        self.index3d.insert(itemId, (x, y, z, x, y, z))
        #προσθέτει το στοιχείο και τις πληροφορίες του στην λίστα που κρατείται με το σύνολο των εισαχθέντων στοιχείων
        self.dataList.append(item)
    #πραγματοποιεί αναζήτηση στο r-tree για τα δεδομένα που έχουν οριστεί στην qbbox που ορίζει ένα query bounding box     
    def search(self, qbbox):
        return list(self.index3d.intersection(qbbox))
#μετατροπή των αρχικών γραμμάτων του surname των στοιχείων σε αριθμούς για χρήση τους ως την συντεταγμένη x στο δέντρο
def letter_normalization(letter):
    letter = normalize('NFD', letter)
    filtered_letter = ''.join(c for c in letter if unicodedata.category(c) != 'Mn')
    return ord(filtered_letter.upper())-65
#εισαγωγή όλων των γραμμών του .csv αρχείου ως στοιχεία στο RTree, χρήση της μεθόδου insert(), μετά από προσδιορισμό των συντεταγμένων
def create_rtree():
    df = pd.read_csv(CSV_PATH)
    rtree = RTree()
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['Surname'][0])
        y = df.iloc[i]['#Awards']
        z = df.iloc[i]['DBLP']
        data = (df.iloc[i]['Surname'], df.iloc[i]['#Awards'], df.iloc[i]['DBLP'], df.iloc[i]['Education'])
        rtree.insert(i, data, x, y, z)
    return rtree

#καθορισμός του query bounding box προσδιορίζοντας το range των συντεταγμένων που θέλουμε να γίνει αναζήτηση
#στο δέντρο με χρήση της μεθόδου search
def query_rtree(rtree, minLetter, maxLetter, minAwards, minDBLP, maxDBLP):
    minLetter = letter_normalization(minLetter)
    maxLetter = letter_normalization(maxLetter)
    qbbox = (minLetter, minAwards, minDBLP, maxLetter, sys.maxsize, maxDBLP)
    matchingIds = rtree.search(qbbox)
    queryResults = []
    #αποθήκευση των αποτελεσμάτων της αναζήτησης σε λίστα και αλφαβητική ταξινόμηση
    for id in matchingIds:
        queryResults.append(rtree.dataList[id])
        queryResults.sort(key=lambda x: x[0])
    return queryResults

#παρόμοια υλοποίηση για διευκόλυνση στο demo.py και testing.py
#τα ορίσματα του range κάθε χαρακτηριστικού είναι λίστα που περιέχει min και max και όχι ξεχωριστές τιμές για το καθένα
def query_rtree_by_range(rtree, Letter_range, minAwards, DBLP_range):
    minLetter = letter_normalization(Letter_range[0])
    maxLetter = letter_normalization(Letter_range[1])
    qbbox = (minLetter, minAwards, DBLP_range[0], maxLetter, sys.maxsize, DBLP_range[1])
    matchingIds = rtree.search(qbbox)
    queryResults = []
    for id in matchingIds:
        queryResults.append(rtree.dataList[id])
        queryResults.sort(key=lambda x: x[0])
    return queryResults
