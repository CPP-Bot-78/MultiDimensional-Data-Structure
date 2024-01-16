from Node1D import Node1D


class RangeTree1D:
    """
    The 1D Range tree for y value
    :param list points: The points of the 1D tree
    """
    def __init__(self, points):
        """Κατασκευή του 1D δέντρου για τα δοθέντα points"""
        self.root = self.build1D(points)

    def insert1D(self, root, y, i_list):
        """Εισαγωγή ενός νέου σημείου στο 1D δέντρο και εφαρμογή της διαδικασίας εξισορρόπησής του
        :param Node1D root: The points of the 1D tree
        :param int y: Tο y-value του κόμβου
        :param list i_list:  H λίστα που πρέπει να εισαχθεί
        :return: New BBST tree
        :rtype: Node1D
        """
        if not root:
            return Node1D(y, [i_list])
        if y == root.y:     # αν υπάρχει ήδη κόμβος με το ίδιο y-value, συγχωνεύστε σε μία λίστα τα i's
            root.merge_i_list([i_list])
        elif y < root.y:    # εισαγωγή του κόμβου στο αριστερό υπο-δέντρο
            root.left = self.insert1D(root.left, y, i_list)
        else:               # εισαγωγή του κόμβου στο δεξί υπο-δέντρο
            root.right = self.insert1D(root.right, y, i_list)

        # Ενημέρωση του ύψους του τρέχοντα κόμβου με βάση τα ύψη των υπο-δέντρων του
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Υπολογισμός του παράγοντα ισορροπίας του τρέχοντα κόμβου
        balance = self.get_balance(root)

        # Αν ο κόμβος είναι "βαρύς" από τα αριστερά
        if balance > 1:
            # Αν το y είναι μεγαλύτερο από το y του αριστερού παιδιού του κόμβου,
            # τότε γίνεται αριστερή περιστροφή στο αριστερό παιδί του κόμβου
            if y > root.left.y:
                root.left = self.left_rotate(root.left)
            # Δεξιά περιστροφή του τρέχοντα κόμβου
            return self.right_rotate(root)

        # Αν ο κόμβος είναι "βαρύς" από τα δεξιά
        if balance < -1:
            # Αν το y είναι μικρότερο από το y του δεξιού παιδιού του κόμβου,
            # τότε γίνεται δεξιά περιστροφή στο δεξί παιδί του κόμβου
            if y < root.right.y:
                root.right = self.right_rotate(root.right)
            # Αριστερή περιστροφή του τρέχοντα κόμβου
            return self.left_rotate(root)

        return root

    def build1D(self, points):
        """ Builds the 1D tree
        :param points: Τα σημεία από τα οποία αποτελείται το δέντρο
        :return: Node assembled
        :rtype: Node1D
        """
        root = None
        for _, y, i in points:
            root = self.insert1D(root, y, i)
        return root

    def get_height(self, node):
        """Συνάρτηση για την επιστροφή του ύψους ενός κόμβου
        :param Node1D node: O κόμβος για τον οποίο ψάχνουμε το ύψος του.
        :return: Το ύψος του κόμβου
        :rtype: int
        """
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Συνάρτηση για την επιστροφή του παράγοντα ισορροπίας ενός κόμβου
        (η διαφορά ύψους μεταξύ των δύο υπο-δέντρων του)
        :param Node1D node: O κόμβος για τον οποίο ψάχνουμε το ύψος του.
        :return: Ο παράγοντας ισορροπίας του κόμβου
        :rtype: int
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, node):
        """Περιστροφή κόμβου προς τα δεξιά
        :param Node1D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node1D
        """
        rotated = node.left
        temp = rotated.right
        rotated.right = node
        node.left = temp
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        rotated.height = max(self.get_height(rotated.left), self.get_height(rotated.right)) + 1
        return rotated

    def left_rotate(self, node):
        """Περιστροφή κόμβου προς τα αριστερά
        :param Node1D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node1D
        """
        rotated = node.right
        temp = rotated.left
        rotated.left = node
        node.right = temp
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        rotated.height = max(self.get_height(rotated.left), self.get_height(rotated.right)) + 1
        return rotated

    def query(self, node, y1, y2, result):
        """Αναζήτηση στο 1D δέντρο
        :param Node1D node:
        :param int y1: Tο 1o y-value της αναζήτησης.
        :param int y2: Tο 2o y-value της αναζήτησης.
        :param list result: Το αποτέλεσμα της αναζήτησης.
        :return: Nothing
        :rtype: None
        """
        if not node:
            return
        if y1 <= node.y <= y2:
            for i in node.i_list:
                result.append((node.y, i))
        if y1 < node.y:
            self.query(node.left, y1, y2, result)
        if y2 > node.y:
            self.query(node.right, y1, y2, result)
