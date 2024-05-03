from collections import deque


class TreeNode:
    """
    Cette classe représente un noeud pour un arbre AVL.
    Il contient la valeur pour un espace résiduel et le(s) niveau(x) associé(s) à cette espace résiduel.
    """
    def __init__(self, residual_space, shelf):
        """
        Initialise une nouvelle instance de la classe TreeNode avec un espace résiduel et un niveau.

        @param residual_space: L'espace résiduel qui sera contenu dans le noeud.
        @param shelf: Le niveau qui sera contenu dans le noeud.
        """
        self.residual_space = residual_space
        self.left = None
        self.right = None
        self.height = 1
        self.list = deque([shelf])  # La liste des niveaux contenus dans le noeud

    def add_shelf(self, shelf):
        """
        Ajoute un niveau dans le noeud.
        Complexité temporelle : 0(1)

        @param shelf: Le niveau à ajouter.
        """
        self.list.append(shelf)


class AVLTree:
    """
    Cette classe représente un arbre AVL contenant les valeurs relatives aux espaces résiduels.
    """

    def insert_node(self, root, residual_space, shelf):
        """
        Permet d'insérer un nouveau noeud dans l'arbre AVl ou de rajouter un niveau
        dans un noeud déjà existant si la valeur pour l'espace résiduel est déjà présente.
        Complexité temporelle : O(log(n))

        @param root : Un noeud de l'arbre AVL (le départ de se fait à la racine).
        @param residual_space : L'espace résiduel à insérer dans l'arbre.
        @param shelf : Le niveau associé à l'espace résiduel.
        @return : L'arbre AVL mis à jour.
        """
        if not root:
            return TreeNode(residual_space, shelf)
        elif residual_space < root.residual_space:
            root.left = self.insert_node(root.left, residual_space, shelf)
        elif residual_space > root.residual_space:
            root.right = self.insert_node(root.right, residual_space, shelf)
        else:
            root.add_shelf(shelf)
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance_factor = self.get_balance(root)
        if balance_factor > 1:
            if residual_space < root.left.residual_space:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance_factor < -1:
            if residual_space > root.right.residual_space:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def delete_node(self, root, residual_space, delete_head):
        """
        Permet de supprimer un noeud de l'arbre AVL. Pour être plus précis, la méthode
        va chercher la valeur pour l'espace résiduel donné et supprimer l'élément en
        en tête de la liste contenant les niveaux. Si jamais la liste est vide, alors
        le noeud sera aussi supprimé.
        Complexité temporelle : O(log(n))

        @param root : Un noeud de l'arbre AVL (le départ de se fait à la racine).
        @param residual_space : L'espace résiduel à supprimer de l'arbre.
        @param delete_head : Un booléen pour contrôler le bon fonctionnement de la méthode.
        @return : L'arbre AVL mis à jour.
        """
        if not root:
            return root
        elif residual_space < root.residual_space:
            root.left = self.delete_node(root.left, residual_space, delete_head)
        elif residual_space > root.residual_space:
            root.right = self.delete_node(root.right, residual_space, delete_head)
        else:
            if delete_head:
                root.list.popleft()
            if len(root.list) != 0 and delete_head:
                return root
            else:
                if root.left is None:
                    return root.right
                elif root.right is None:
                    return root.left
                temp = self.get_min_value_node(root.right)
                root.residual_space = temp.residual_space
                root.list = temp.list
                root.right = self.delete_node(root.right, temp.residual_space, False)
        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance_factor = self.get_balance(root)

        if balance_factor > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        if balance_factor < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        return root

    def left_rotate(self, z):
        """
        Fonction permettant d'effectuer une rotation vers la gauche sur un noeud de l'arbre AVL.
        Complexité temporelle : O(1)

        @param z : Un noeud de l'arbre AVL.
        @return : L'arbre AVL mis à jour.
        """
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        """
        Fonction permettant d'effectuer une rotation vers la droite sur un noeud de l'arbre AVL.
        Complexité temporelle : O(1)

        @param z : Un noeud de l'arbre AVL.
        @return : L'arbre AVL mis à jour.
        """
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        """
        Fonction permettant d'obtenir la hauteur d'un noeud de l'arbre AVL.
        Complexité temporelle : O(1)

        @param root : Un noeud de l'arbre AVL.
        @return : La hauteur du noeud.
        """
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        """
        Fonction permettant d'obtenir la balance d'un noeud de l'arbre AVL.
        Complexité temporelle : O(1)

        @param root : Un noeud de l'arbre AVL.
        @return : La balance du noeud.
        """
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        """
        Fonction permettant d'obtenir un noeud de l'arbre AVL contenant l'espace résiduel
        minimal en partant d'un certain noeud donné.
        Complexité temporelle : O(log(n))

        @param root : Un noeud de l'arbre AVL.
        @return : Le noeud contenant l'espace résiduel minimal.
        """
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def pre_order(self, root):
        """
        Affichage de l'arbre AVL avec un parcours préfixe.
        Complexité temporelle : O(n)

        @param root : Un noeud de l'arbre AVL.
        """
        if not root:
            return
        print("{0} ".format(root.residual_space), end="")
        print(root.list)
        self.pre_order(root.left)
        self.pre_order(root.right)
