from range_tree import RangeTree1D as RangeTree1D


class Node2D:
    """Ο Κόμβος που αποθηκεύει τα x.
    :param int x: Tο x-value του κόμβου.
    :param list points: Η λίστα με τα σημεία που έχουν το ίδιο χ
    """
    def __init__(self, x, points):
        self.x = x
        # το 1D δέντρο του κόμβου που περιέχει τα σημεία που έχουν το ίδιο x
        self.y_tree = RangeTree1D.RangeTree1D(points)
        self.left = None    # ο αριστερός κόμβος
        self.right = None   # ο δεξιός κόμβος
        self.height = 1     # το αρχικό ύψος του κόμβου

    def merge_point(self, y, i):
        """Συγχώνευση ενός σημείου με την ίδια συντεταγμένη x στο y_tree του κόμβου
        :param int y: Tο y-value του κόμβου από το y_tree
        :param list i: Η λίστα με των σημείων του δέντρου
        :returns: None
        """
        self.y_tree.insert1D(self.y_tree.root, y, i)
