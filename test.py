class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.is_end_of_word = False

    def insert(self, word, index):
        if word[index] < self.char:
            if self.left is None:
                self.left = TSTNode(word[index])
            self.left.insert(word, index)
        elif word[index] > self.char:
            if self.right is None:
                self.right = TSTNode(word[index])
            self.right.insert(word, index)
        elif index < len(word) - 1:
            if self.middle is None:
                self.middle = TSTNode(word[index + 1])
            self.middle.insert(word, index + 1)
        else:
            self.is_end_of_word = True

    def search(self, word, index, exact=False):
        if word[index] < self.char:
            if self.left is None:
                return False
            return self.left.search(word, index, exact)
        elif word[index] > self.char:
            if self.right is None:
                return False
            return self.right.search(word, index, exact)
        elif index < len(word) - 1:
            if self.middle is None:
                return False
            return self.middle.search(word, index + 1, exact)
        elif exact:
            return self.is_end_of_word
        return True

    def get_all_words(self, prefix, words):
        if self.is_end_of_word:
            words.append(prefix + self.char)
        if self.left is not None:
            self.left.get_all_words(prefix, words)
        if self.middle is not None:
            self.middle.get_all_words(prefix + self.char, words)
        if self.right is not None:
            self.right.get_all_words(prefix, words)

    def _to_string(self, indent='       '):
        repr_str = indent + repr(self)

        if self.left is not None:
            repr_str += '\n_lt_:' + self.left._to_string(indent + '  ')
        if self.middle is not None:
            repr_str += '\n_eq_:' + self.middle._to_string(indent + '  ')
        if self.right is not None:
            repr_str += '\n_gt_:' + self.right._to_string(indent + '  ')
        return repr_str

    def __repr__(self):
        return f'char: {self.char}, terminates: {self.is_end_of_word}'


class TernarySearchTree:
    def __init__(self):
        self._root = None
        self._terminates = False

    def insert(self, word):
        if word == "":
            self._terminates = True
        else:
            if self._root is None:
                self._root = TSTNode(word[0])
            self._root.insert(word, 0)

    def search(self, word, exact=False):
        if word == '':
            return not exact
        elif self._root is None:
            return False
        return self._root.search(word, 0, exact)

    def all_strings(self):
        if self._terminates:
            words = [""]
        else:
            words = []
        if self._root is not None:
            self._root.get_all_words("", words)
        return words

    def __len__(self):
        if self._root is None:
            return 0
        else:
            return len(self.all_strings())

    def __repr__(self):
        if self._root is None:
            return 'empty tree'
        else:
            return f'terminates: {self._terminates} \n' + self._root._to_string()


tst = TernarySearchTree()
tst.insert('abc')
print(tst.search('', exact=True))


tst = TernarySearchTree()
with open('data/search_trees/insert_words.txt') as file:
    words = [
        line.strip() for line in file
    ]
for word in words:
    tst.insert(word)
unique_words = set(words)
print(unique_words)

for word in unique_words:
    for i in range(len(word), 0, -1):
        prefix = word[:i]
        print(prefix)
        if prefix not in unique_words:
            assert not tst.search(prefix, exact=True), f'{prefix} found'