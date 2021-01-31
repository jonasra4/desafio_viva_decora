class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

        self.extension = None
        self.size = 0
        self.lines = 0


    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = '|  ' * (self.get_level()-1)
        prefix = spaces + "|__ " if self.parent else ""
        
        if self.extension is not None:
            print(prefix + self.data + " (" + str(self.lines)+ " linhas)  " + str(self.size) + "  "  + self.extension)
        else:
            print(prefix + "[" + self.data + "]")

        if self.children:
            for child in self.children:
                child.print_tree()

    def convert_to_bytes(self):
        num_unity = self.size.split(' ')
        
        num = float(num_unity[0])
        unity = num_unity[1]

        if unity == 'Bytes' or unity == 'Byte':
            self.size = num
        elif unity == 'KB':
            self.size = 1000 * num
        elif unity == 'MB':
            self.size = 1000000 * num
        elif unity == 'GB':
            self.size = 1000000000 * num

    def convert_to_extension(self):
        ext = self.data.split('.')
        if len(ext) >= 2 and ext[0]:
            self.extension = ext[-1]
        else:
            self.extension = '<outros>'
      
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    # {
    #     js = [lines, bytes ]
    # }
    rept = {}
    def report(self):
        if self.extension:
            if self.extension in self.rept:
                self.rept[self.extension][0] += self.lines
                self.rept[self.extension][1] += self.size
            else:
                self.rept[self.extension] = [self.lines, self.size]
                s
        if self.children:
            for child in self.children:
                child.report()