class Location:

    def __init__(self, section, book):
        self.section = section
        self.book = book


    def __eq__(self, other):
        print(self)
        print(other)
        if self.section == other.section and self.book == other.book:
            return True
        return False


    def __repr__(self):
        return f"{self.book}, section: {str(self.section)}"


    def __hash__(self):
        hash = ""
        for c in str(self):
            hash = f"{hash}{ord(c)}"
        return int(hash)
