from Node3D import Node3D


class RangeTree3D:
    def __init__(self, points):
        self.root = self.build3D(points)

    def insert3D(self, root, x, y, z, i_list, points):
        """Εισαγωγή ενός νέου σημείου στο 2D δέντρο και εφαρμογή της διαδικασίας
        εξισορρόπησής του
        :param Node2D root: The points of the 2D tree
        :param int x: Tο x-value του κόμβου
        :param int y: Tο y-value του κόμβου
        :param int z: Tο z-value του κόμβου
        :param list i_list:  H λίστα που πρέπει να εισαχθεί
        :param list points: Tα σημεία για την κατασκευή του 2D δέντρου
        :return: New BBST tree
        :rtype: Node2D
        """
        if not root:
            return Node3D(x, [(x, y, z, i_list)])
        if z == root.z:     # αν υπάρχει ήδη κόμβος με το ίδιο x-value, κάνε εισαγωγή κόμβου στο αντίστοιχο y_tree
            root.xy_tree.root = root.xy_tree.insert2D(root.xy_tree.root, x, y, i_list)
        elif z < root.z:    # εισαγωγή του κόμβου στο αριστερό υπο-δέντρο
            root.left = self.insert3D(root.left, x, y, i_list, [(x, y, i_list)])
        else:               # εισαγωγή του κόμβου στο δεξί υπο-δέντρο
            root.right = self.insert3D(root.right, x, y, i_list, [(x, y, i_list)])

        # Ενημέρωση του ύψους του τρέχοντα κόμβου με βάση τα ύψη των υπο-δέντρων του
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Υπολογισμός του παράγοντα ισορροπίας του τρέχοντα κόμβου
        balance = self.get_balance(root)

        # Αν ο κόμβος είναι "βαρύς" από τα αριστερά
        if balance > 1:
            # Αν το x είναι μεγαλύτερο από το x του αριστερού παιδιού του κόμβου,
            # τότε γίνεται αριστερή περιστροφή στο αριστερό παιδί του κόμβου
            if z > root.left.z:
                root.left = self.left_rotate(root.left)
            # Αριστερή περιστροφή του τρέχοντα κόμβου
            return self.right_rotate(root)

        # Αν ο κόμβος είναι "βαρύς" από τα δεξιά
        if balance < -1:
            # Αν το x είναι μικρότερο από το x του δεξιού παιδιού του κόμβου,
            # τότε γίνεται δεξιά περιστροφή στο δεξί παιδί του κόμβου
            if z < root.right.z:
                root.right = self.right_rotate(root.right)
            # Δεξιά περιστροφή του τρέχοντα κόμβου
            return self.left_rotate(root)

        return root

    def build3D(self, points):
        """ Builds the 2D tree
        :param points: Τα σημεία από τα οποία αποτελείται το δέντρο
        :return: Node assembled
        :rtype: Node2D
        """
        root = None
        for point in points:
            x, y, z, i = point
            root = self.insert3D(root, x, y, z, i, [point])
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
        :param Node3D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node3D
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
        :param Node3D node: ο κόμβος που θέλουμε να περιστραφεί
        :return: Ο περιστραμμένος κόμβος
        :rtype: Node3D
        """
        rotated = node.right
        temp = rotated.left
        rotated.left = node
        node.right = temp
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        rotated.height = max(self.get_height(rotated.left), self.get_height(rotated.right)) + 1
        return rotated

    def query(self, node, x1, x2, y1, y2, z1, z2, result):  # TODO
        """Αναζήτηση στο 3D δέντρο
         :param Node3D node:
         :param int x1: Tο 1o x-value της αναζήτησης.
         :param int x2: Tο 2o x-value της αναζήτησης.
         :param int y1: Το 1o y-value της αναζήτησης.
         :param int y2: Tο 2o y-value της αναζήτησης.
         :param int z1: Tο 1o z-value της αναζήτησης.
         :param int z2: Το 2o z-value της αναζήτησης.
         :param list result: Το αποτέλεσμα της αναζήτησης.
         :return: Nothing
         :rtype: None
         """
        if not node:
            return
        if z1 <= node.z <= z2:
            z_result = []
            node.xy_tree.query(node.xy_tree.root, x1, x2, y1, y2, z_result)
            for x, y, i in z_result:
                result.append((x, y, node.z, i))
        if z1 < node.z:
            self.query(node.left, x1, x2, y1, y2, z1, z2, result)
        if z2 > node.z:
            self.query(node.right, x1, x2, y1, y2, z1, z2, result)