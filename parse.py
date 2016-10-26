

class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.parse()

    def parse(self):
        print(self.filename)

if __name__ == "__main__":
    Parser('test')
