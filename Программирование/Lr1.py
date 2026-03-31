def gen_bin_rec_tree(root, height):
    
    tree = {}

    def build_tree(node, current_height):
        if current_height == 0:
            return node

        tree[node] = []
        left_child = node + 1
        right_child = node - 1

        left_subtree = build_tree(left_child, current_height - 1)
        right_subtree = build_tree(right_child, current_height - 1)

        tree[node].extend([left_subtree, right_subtree])
        return node

    build_tree(root, height)
    return tree


def main():
    print("Рекурсивное бинарное дерево:")
    print(gen_bin_rec_tree(root=13, height=3))

if __name__ == "__main__":
    main()


#Нерекурсивная функция
def gen_bin_nec_tree(height: int, root: int, left_leaf = lambda x: x + 1, right_leaf = lambda x: x - 1) -> dict:

    if height <= 0:
        return {}

    tree = {root: []}
    stack = [(root, height)]

    while stack:
        node, current_height = stack.pop()

        if current_height >= 1:
            left_value = left_leaf(node)
            right_value = right_leaf(node)

            if left_value not in tree:
                tree[left_value] = []
            if right_value not in tree:
                tree[right_value] = []

            tree[node].append({left_value: []})
            tree[node].append({right_value: []})

            stack.append((left_value, current_height - 1))
            stack.append((right_value, current_height - 1))

    return tree

def main():
    print("Нерекурсивное бинарное дерево:")
    print(gen_bin_nec_tree(root=13, height=3))

if __name__ == "__main__":
    main()