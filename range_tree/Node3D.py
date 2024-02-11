from range_tree import RangeTree2D as R2D


class Node3D:
    """Ο Κόμβος που αποθηκεύει τα z.
    :param int z: Tο z-value του κόμβου.
    :param list points: Η λίστα με τα σημεία που έχουν το ίδιο z
    """
    def __init__(self, z, points):
        self.z = z
        # το 2D δέντρο του κόμβου που περιέχει τα σημεία που έχουν το ίδιο x
        self.xy_tree = R2D.RangeTree2D(points[:-2])
        self.left = None  # ο αριστερός κόμβος
        self.right = None  # ο δεξιός κόμβος
        self.height = 1  # το αρχικό ύψος του κόμβου

    def merge_point(self, x, y, i):
        """Συγχώνευση ενός σημείου με την ίδια συντεταγμένη x στο y_tree του κόμβου
        :param int y: Tο y-value του κόμβου από το y_tree
        :param int x: Tο y-value του κόμβου από το xy_tree
        :param list i: Η λίστα με των σημείων του δέντρου
        :returns: None
        """
        self.xy_tree.insert2D(self.xy_tree.root, x, y, i, [])
