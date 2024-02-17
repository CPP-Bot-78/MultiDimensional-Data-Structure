import pandas as pd
import os

# Ενα Octree λειτουργεί όπως ένα Quadtree, απλά για 3 διαστάσεις. (2D -> 3D)
# Χωρίζει εναν τρισδιάστατο χώρο (κύβο) σε 8 μικρότερους κύβους (octants) και εισάγει τα δεδομένα με βάση τις x,y,z συντεταγμένες
# Για τον διαχωρισμό χρησιμοποιούμε την τεχνική της μέσης τιμής (median) για την ομοιόμορφη κατανομή των δεδομένων

# Αρχικοποίηση του leaf threshold, το οποίο καθορίζει πότε θα χωριστούν τα octants 
LEAF_THRESHOLD = 50

# Η κλάση Octant περιγράφει κάθε node του octree
class Octant:
    def __init__(self, x_bounds, y_bounds, z_bounds, leaf_node):
        # Τα x, y και z bounds αντιστοιχούν στα εύρη κάθε octant και δείχνουν που ανήκουν τα δεδομένα
        # Όταν το leaf_node είναι True μπορούμε να αποθηκεύσουμε δεδομένα μεσα (Child), όταν είναι False περιέχει 8 octants (Parent)
        # Τα median καθορίζουν τα όρια του κάθε octant
        # Τα data αποθηκεύουν τα δεδομένα κάθε child node
        # Κάθε parent node έχει 8 children nodes
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.z_bounds = z_bounds
        self.leaf_node = leaf_node
        self.medians = []
        self.data = []
        self.children = [None] * 8
        
# H κλάση Octree εμπεριέχει όλα τα αναγκαία functions και χρησιμοποιεί την κλάση octant
class Octree:
    def __init__(self, x_bounds, y_bounds, z_bounds, leaf_node):
        self.root = Octant(x_bounds, y_bounds, z_bounds, leaf_node)

    def __str__(self):
        return "OctTree"

    def split_octant(self, octant):
        # Υπολογισμός και αποθήκευση median για κάθε μεταβλητή, για να καθοριστεί σε ποιό octant πάνε τα δεδομένα
        x_list, y_list, z_list = split_list(octant.data)
        x_median = find_median(x_list)
        y_median = find_median(y_list)
        z_median = find_median(z_list)
        octant.medians = [x_median, y_median, z_median]

        # Χωρίζουμε το Parent node σε 8 children nodes
        # Ο διαχορισμός δουλεύει με μια 3-bit δυαδική λογική, όπου 0=min,median και 1=median,max [000,001,010,011,100,101,110,111]
        octant.children[0] = Octant((octant.x_bounds[0], x_median), (octant.y_bounds[0], y_median),(octant.z_bounds[0], z_median), True)
        octant.children[1] = Octant((octant.x_bounds[0], x_median), (octant.y_bounds[0], y_median),(z_median, octant.z_bounds[1]), True)
        octant.children[2] = Octant((octant.x_bounds[0], x_median), (y_median, octant.y_bounds[1]),(octant.z_bounds[0], z_median), True)
        octant.children[3] = Octant((octant.x_bounds[0], x_median), (y_median, octant.y_bounds[1]),(z_median, octant.z_bounds[1]), True)
        octant.children[4] = Octant((x_median, octant.x_bounds[1]), (octant.y_bounds[0], y_median),(octant.z_bounds[0], z_median), True)
        octant.children[5] = Octant((x_median, octant.x_bounds[1]), (octant.y_bounds[0], y_median),(z_median, octant.z_bounds[1]), True)
        octant.children[6] = Octant((x_median, octant.x_bounds[1]), (y_median, octant.y_bounds[1]),(octant.z_bounds[0], z_median), True)
        octant.children[7] = Octant((x_median, octant.x_bounds[1]), (y_median, octant.y_bounds[1]),(z_median, octant.z_bounds[1]), True)


    def find_child_index(self, datapoint, octant):
        # Βρίκουμε ποιό απο τα 8 children εμπεριέχει τα datapoints
        # Ίδια λογική με την split_octant, προσθέτουμε στην μεταβλητή child τον αντίστοιχο αριθμό για να ορίσουμε που ταιριάζει
        # Π.χ.: Αν x μικρότερο του median, ανήκει στα πρώτα 4 παιδιά
        # Aν y μικρότερο του median, ανήκει στα παιδιά 0,1,4,5
        # Αν z μεγαλύτερο του median, ανήκει στα παιδιά με μονό αριθμό
        index, x, y, z = datapoint
        x_median, y_median, z_median = octant.medians
        child = 0
        
        if x > x_median:
                child += 4
        if y > y_median:
                child += 2
        if z > z_median:
                child += 1

        return child


    def insert(self, datapoint, octant=None):
        # H insert τοποθετεί το datapoint στο σωστό octant
        # Αν βρισκόμαστε σε leaf_node προσθέτει τα δεδομένα
        # Αν φτάσαμε το LEAF_THRESHOLD χωρίζουμε τα octant και εισάγουμε τα δεδομένα στα children που δημιουργήθηκαν
        # Aν είμαστε σε Parent node βρίσκουμε το σωστό child και καλούμε αναδρομικά την insert για να εισάγουμε την τιμή
        if octant is None:
            octant = self.root

        if octant.leaf_node:
            octant.data.append(datapoint)

            # Αν φτάσαμε το leaf threshold
            if len(octant.data) == LEAF_THRESHOLD:
                octant.leaf_node = False
                self.split_octant(octant)

                # Κανε αναδρομικά insert στο child
                for data in octant.data:
                    child = self.find_child_index(data, octant)
                    self.insert(data, octant.children[child])
                octant.data = []

            return

        # Βρες το σωστό child index
        child = self.find_child_index(datapoint, octant)
        # Κάλεσε αναδρομικά την insert για το σωστό παιδί
        self.insert(datapoint, octant.children[child])
    
    
    def search(self, search_bounds, octant=None):
        # Η συνάρτηση αναζήτησης ελέγχει πρώτα αν τα όρια αναζήτησης τέμνονται με τα όρια του octant
        # Έτσι μειώνετε το repetition χωρίς να χρειάζεται έλεγχος έξω από το seach_bound box
        # Αν είναι μεσα το box και το octant ειναι child node βρες τα datapoints
        # Αν είναι parent node ψάξε αναδρομικά τα παιδιά του
        x_min, x_max, y_min, y_max, z_min, z_max = search_bounds
        found = []

        if octant is None:
            octant = self.root

        # Ελέγχουμε αν το search box τέμνει τα octant.bounds
        if (
            x_max < octant.x_bounds[0] or x_min > octant.x_bounds[1] or
            y_max < octant.y_bounds[0] or y_min > octant.y_bounds[1] or
            z_max < octant.z_bounds[0] or z_min > octant.z_bounds[1]
        ):
            # Δεν τέμνουν, επέστρεψε
            return found
        # Ελέγχουμε αν το octant είναι child node και ψάχνουμε για τα datapoints
        if octant.leaf_node:
            for data_point in octant.data:
                x, y, z = data_point[1:]
                if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                    found.append(data_point[0])
        else:
            # Αν είναι parent node, ψάξε αναδρομικά τα παιδιά του
            for child in octant.children:
                found.extend(self.search(search_bounds, child))

        return found

    

def find_median(my_list):
    # Βρίσκει την μέση τιμή μιας λίστας
    sort = sorted(my_list)
    length = len(my_list)
    
    # Αν το μήκος είναι ζυγό, βρές το μέσο των δύο μεσαίων τιμών
    if length % 2 ==0:
        median1 = sort[(length // 2) - 1]
        median2 = sort[length // 2]
        median = (median1 + median2) // 2
    # Αν το μήκος είναι περιττό, η μέση τιμή είναι η μεσαία τιμή
    else:
        median= sort[length // 2]
    
    return median


def split_list(my_list):
    # Χωρίζει μία λίστα σε τρεις, μία για κάθε συντεταγμένη(x,y,z)
    x = [point[1] for point in my_list]
    y = [point[2] for point in my_list]
    z = [point[3] for point in my_list]

    return x, y, z


def extract_data(file_csv):
    # Extract τα δεδομένα απο το csv και επέστρεψε 4 λίστες
    df = pd.read_csv(file_csv)
    
    # Μετροπή του πρώτου γράμματος του επιθέτου σε αριθμό[Α=0,Β=1,C=2...]
    df['Surname'] = df['Surname'].apply(lambda x: ord(x[0].lower()) - 97)

    index_list = df['Index'].tolist()
    surname_list = df['Surname'].tolist()
    awards_list = df['#Awards'].tolist()
    dblp_list = df['DBLP'].tolist()
    
    return index_list, surname_list, awards_list, dblp_list


def build_octree():
    # Κατασκευή του Octree και εισαγωγή των δεδομένων
    try:
        csv_file = 'scripts/computer_scientists_data2.csv'
        index, surname, awards, dblp = extract_data(csv_file)
    except Exception as e:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        home_dir = os.path.dirname(script_directory)
        csv_file = os.path.join(home_dir, 'computer_scientists_data2.csv')
        index, surname, awards, dblp = extract_data(csv_file)

    cs_data = list(zip(index, surname, awards, dblp))

    ot = Octree([min(surname),max(surname)], [min(awards),max(awards)], [min(dblp),max(dblp)], False)
    # Αρχικοποίηση root
    ot.root.data = cs_data
    ot.split_octant(ot.root)
    # Εισαγωγή των δεδομένων
    for datapoint in cs_data:
        ot.insert(datapoint)

    return ot


def query_octree(octree, x_range, y_min, z_range):
    try:
        csv_file = 'scripts/computer_scientists_data2.csv'
        index, surname, awards, dblp = extract_data(csv_file)
        df = pd.read_csv(csv_file)
    except Exception as e:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        home_dir = os.path.dirname(script_directory)
        csv_file = os.path.join(home_dir, 'computer_scientists_data2.csv')
        index, surname, awards, dblp = extract_data(csv_file)
        df = pd.read_csv(csv_file)

    # Αναγκαίες μετατροπές των δεδομένων (Εύρεση y_max, Μεταροπή χαρακτήρων σε αριθμούς)
    y_max = df['#Awards'].max()
    y_range = [y_min, y_max]
    x_range = [ord(letter.lower()) - 97 for letter in x_range]
    
    # Κάνε αναζήτηση του octree για το δοσμένα ranges χρησιμοποιόντας bounding box
    search_bounds = (x_range[0], x_range[1], y_range[0], y_range[1], z_range[0], z_range[1])
    found = octree.search(search_bounds)

    # Δημιουργία λίστας με τα indexes που βρήκαμε
    index_list = pd.Series(found).explode().tolist()

    # Εύρεση τιμών με βάση το index
    filter_by_index = df.loc[index_list]
    result = filter_by_index[['Surname', '#Awards', 'DBLP',  'Education']].values.tolist()

    return result
