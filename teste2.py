class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = '\t' * self.get_level()
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    

def build_product_tree():
    root = TreeNode("Projeto")

    # 1 no
    ci = TreeNode("ci")
    
   
    # 1 no
    src = TreeNode("src")
    js  = TreeNode("js")
    api = TreeNode("api")
    api.add_child(TreeNode("vi"))
    api.add_child(TreeNode("v2"))
    js.add_child(api)
    src.add_child(js)
    src.add_child(TreeNode("aaa"))

   
    root.add_child(ci)
    root.add_child(src)

    root.print_tree()

if __name__ == '__main__':
    build_product_tree()