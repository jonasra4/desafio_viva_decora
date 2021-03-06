class TreeFile:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.path = None
        self.extension = None
        self.size = None
        self.lines = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def convert_size_to_bytes(self):
        try:
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
        except:
            self.size = 0
        
    def convert_to_extension(self):
        ext = self.data.split('.')
        if len(ext) >= 2 and ext[0]:
            self.extension = ext[-1]
        else:
            self.extension = '<outros>'
      
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
