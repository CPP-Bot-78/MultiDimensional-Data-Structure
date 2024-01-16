class Node1D:
    """Ο Κόμβος που αποθηκεύει τα y.
        :param int y: Tο y-value του κόμβου.
        :param list i_list: H λίστα με τους αριθμούς των rows του dataframe που αντιστοιχούν στα (x, y)
        """
    def __init__(self, y, i_list):
        self.y = y
        self.i_list = i_list
        self.left = None  # ο αριστερός κόμβος
        self.right = None  # ο δεξιός κόμβος
        self.height = 1  # το αρχικό ύψος του κόμβου

    def merge_i_list(self, i_list):
        """Συγχώνευση μιας λίστας με την υπάρχουσα λίστα του κόμβου και αφαίρεση διπλότυπων
        :param list i_list: H λίστα με τους αριθμούς των rows του dataframe που αντιστοιχούν στα (x, y)
        :returns: None
        """
        self.i_list.extend(i_list)
        self.i_list = list(set(self.i_list))
