from range_tree import RangeTree2D as R2D


class Node3D:
    """Ο Κόμβος που αποθηκεύει τα z.
    :param int z: Tο z-value του κόμβου.
    :param list points: Η λίστα με τα σημεία που έχουν το ίδιο z
    """
    def __init__(self, z, points):
        self.z = z
        self.xy_tree = R2D.RangeTree2D(points)
        self.left = None  # ο αριστερός κόμβος
        self.right = None  # ο δεξιός κόμβος
        self.height = 1  # το αρχικό ύψος του κόμβου
