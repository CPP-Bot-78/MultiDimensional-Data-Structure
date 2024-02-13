from range_tree import Node2D as N2D
# from RangeTree1D import RangeTree1D


class RangeTree2D:

    def __init__(self, points):
        """Κατασκευή του 2D δέντρου για τα δοθέντα points"""
        self.root = self.build2D(points)

    def insert2D(self, root, x, y, i_list):
        """Εισαγωγή ενός νέου σημείου στο 2D δέντρο και εφαρμογή της διαδικασίας
        εξισορρόπησής του
        :param Node2D root: The points of the 2D tree
        :param int x: Tο x-value του κόμβου
        :param int y: Tο y-value του κόμβου
        :param int i_list:  To index του dataframe
        :return: New BBST tree
        :rtype: Node2D
        """
        if not root:
            return N2D.Node2D(x, [(x, y, None, i_list)])
        if x == root.x:     # αν υπάρχει ήδη κόμβος με το ίδιο x-value, κάνε εισαγωγή κόμβου στο αντίστοιχο y_tree
            root.y_tree.root = root.y_tree.insert1D(root.y_tree.root, y, i_list)
        elif x < root.x:    # εισαγωγή του κόμβου στο αριστερό υπο-δέντρο
            root.left = self.insert2D(root.left, x, y, i_list)
        else:               # εισαγωγή του κόμβου στο δεξί υπο-δέντρο
            root.right = self.insert2D(root.right, x, y, i_list)

        # Ενημέρωση του ύψους του τρέχοντα κόμβου με βάση τα ύψη των υπο-δέντρων του
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Υπολογισμός του παράγοντα ισορροπίας του τρέχοντα κόμβου
        balance = self.get_balance(root)

        # Αν ο κόμβος είναι "βαρύς" από τα αριστερά
        if balance > 1:
            # Αν το x είναι μεγαλύτερο από το x του αριστερού παιδιού του κόμβου,
            # τότε γίνεται αριστερή περιστροφή στο αριστερό παιδί του κόμβου
            if x > root.left.x:
                root.left = self.left_rotate(root.left)
            # Αριστερή περιστροφή του τρέχοντα κόμβου
            return self.right_rotate(root)

        # Αν ο κόμβος είναι "βαρύς" από τα δεξιά
        if balance < -1:
            # Αν το x είναι μικρότερο από το x του δεξιού παιδιού του κόμβου,
            # τότε γίνεται δεξιά περιστροφή στο δεξί παιδί του κόμβου
            if x < root.right.x:
                root.right = self.right_rotate(root.right)
            # Δεξιά περιστροφή του τρέχοντα κόμβου
            return self.left_rotate(root)

        return root

    def build2D(self, points):
        """ Builds the 2D tree
        :param points: Τα σημεία από τα οποία αποτελείται το δέντρο
        :return: Node assembled
        :rtype: Node2D
        """
        root = None
        for point in points:
            x, y, _, i = point
            root = self.insert2D(root, x, y, i)
        return root

    def get_height(self, node):
        """Συνάρτηση για την επιστροφή του ύψους ενός κόμβου
        :param Node2D node: O κόμβος για τον οποίο ψάχνουμε το ύψος του.
        :return: Το ύψος του κόμβου
        :rtype: int
        """
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Συνάρτηση για την επιστροφή του παράγοντα ισορροπίας ενός κόμβου
        (η διαφορά ύψους μεταξύ των δύο υπο-δέντρων του)
        :param Node2D node: O κόμβος για τον οποίο ψάχνουμε το ύψος του.
        :return: Ο παράγοντας ισορροπίας του κόμβου
        :rtype: int
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, node):
        """Περιστροφή κόμβου προς τα δεξιά
        :param Node2D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node2D
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
        :param Node2D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node2D
        """
        rotated = node.right
        temp = rotated.left
        rotated.left = node
        node.right = temp
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        rotated.height = max(self.get_height(rotated.left), self.get_height(rotated.right)) + 1
        return rotated

    def query(self, node, x1, x2, y1, y2, result):
        """Αναζήτηση στο 2D δέντρο
         :param Node2D node:
         :param int x1: Tο 1o x-value της αναζήτησης.
         :param int x2: Tο 2o x-value της αναζήτησης.
         :param int y1: Το 1o y-value της αναζήτησης.
         :param int y2: Tο 2o y-value της αναζήτησης.
         :param list result: Το αποτέλεσμα της αναζήτησης.
         :return: Nothing
         :rtype: None
         """
        if not node:
            return
        if x1 <= node.x <= x2:
            y_result = []
            node.y_tree.query(node.y_tree.root, y1, y2, y_result)
            for y, i in y_result:
                result.append((node.x, y, i))
        if x1 < node.x:
            self.query(node.left, x1, x2, y1, y2, result)
        if x2 > node.x:
            self.query(node.right, x1, x2, y1, y2, result)
