from collections import deque

# Create a tree node


class TreeNode:
    def __init__(self, residual_space, shelf):
        self.residual_space = residual_space
        self.left = None
        self.right = None
        self.height = 1
        self.list = deque([shelf])

    def add_shelf(self, shelf):
        self.list.append(shelf)


class AVLTree:

    # Function to insert a node
    def insert_node(self, root, residual_space, shelf):

        # Find the correct location and insert the node
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

        # Update the balance factor and balance the tree
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

    # Function to delete a node
    def delete_node(self, root, residual_space, delete_head):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif residual_space < root.residual_space:
            root.left = self.delete_node(root.left, residual_space, delete_head)
        elif residual_space > root.residual_space:
            root.right = self.delete_node(root.right, residual_space, delete_head)
        else:
            if delete_head:
                root.list.popleft()
            if len(root.list) != 0:
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

        # Update the balance factor of nodes
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance_factor = self.get_balance(root)

        # Balance the tree
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

    # Function to perform left rotation
    def left_rotate(self, z):
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Function to perform right rotation
    def right_rotate(self, z):
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Get the height of the node
    def get_height(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def pre_order(self, root):
        if not root:
            return
        print("{0} ".format(root.residual_space), end="")
        print(root.list)
        self.pre_order(root.left)
        self.pre_order(root.right)
