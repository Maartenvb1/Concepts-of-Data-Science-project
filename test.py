class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.is_end_of_word = False

    def insert(self, word, index): # Method (called on TST node) for inserting string with given index on node in tree
        if word[index] < self.char: # Check if value of letter in string is less than value of node
            if self.left is None: # Check if node has no left child
                self.left = TSTNode(word[index]) # Create new left child node for the current character of string
            self.left.insert(word, index) # Insert character of string on left node
        elif word[index] > self.char: # Check if character value is greater than value of node character
            if self.right is None: # Check if right child does not exist
                self.right = TSTNode(word[index]) # Create right child  for node 
            self.right.insert(word, index) # Insert string on right child 
        elif index < len(word) - 1: # Check if current string character is not last character of string 
            if self.middle is None: # Check whether current node has no middle child
                self.middle = TSTNode(word[index + 1]) # Create new middle child for node, which is the next character in the string
            self.middle.insert(word, index + 1) # Insert word in middle child node and continue to next character in string
        else: # End of word has been reached
            self.is_end_of_word = True # Set end-of-word flag to true

    def search(self, word, index, exact=False):
        if word[index] < self.char: # Check whether value of string character is less than value of current node character (go to left child)
            if self.left is None: # Check whether node has no left child
                return False # Searched string is not in TST
            # Continue search on left child node
            return self.left.search(word, index, exact)
        elif word[index] > self.char: # Check whether value of string character is greater than value of current node character (go to right child)
            if self.right is None: # Check whether node has no right child
                return False # Searched string is not in TST
            return self.right.search(word, index, exact) # Continue search on right child node
        elif index < len(word) - 1: # Check if current string char is not last in string
            if self.middle is None: # Check whether node has no middle child
                return False # Searched string is not in TST
            return self.middle.search(word, index + 1, exact) # Continue search on middle child node, and evaluate next character in string
        elif exact: # End of searched string has been reached, check whether searched string must exactly be in TST
            return self.is_end_of_word # Returns true if the current node is flagged as end of word (string is exactly in TST), False if only prefix of string is in TST
        return True # If only prefix search is required, return True when leaf node has been reached

    def get_all_words(self, prefix, words): # This method recursively explores each branch of the tree, by iteratively concatonating a newly found letter to a current prefix, and appends the complete word to the words list once it has reached a terminating node
        if self.is_end_of_word: # Recursive base (stopping) condition, when current node is leaf node
            words.append(prefix + self.char) # Concatonate prefix + leaf node character and append to words list
        if self.left is not None: # Check existence of left child node
            self.left.get_all_words(prefix, words) # Apply method on left child node
        if self.middle is not None: # Check existence of middle child node
            self.middle.get_all_words(prefix + self.char, words) # Concatonate prefix + current node character, and apply method on middle child node with updated prefix
        if self.right is not None: # Check existence of right child node
            self.right.get_all_words(prefix, words) # Apply method on right child node

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
    def __init__(self): # Instantiate TST object
        self._root = None
        self._terminates = False

    def insert(self, word): # Operation for inserting a new string in the TST
        if word == "": # Check if the string is empty
            self._terminates = True
        else: 
            if self._root is None: # Check whether the TST has no root node
                self._root = TSTNode(word[0]) # Assign the first letter of the string as root node in case there was none
            self._root.insert(word, 0) # Insert the new string via the root node

    def search(self, word, exact=False):
        if word == '': # Check if searched string is empty
            return not exact 
        elif self._root is None: # Check whether TST contains no root node
            return False 
        return self._root.search(word, 0, exact) # Apply search on root node

    def all_strings(self):
        if self._terminates: # Check whether TST is empty
            words = [""] # Make list with empty string
        else:
            words = [] # Instantiate empty list
        if self._root is not None: # Check existence of root node
            self._root.get_all_words("", words) # Apply recursive string retrieval on root node, and provide an empty prefix & list
        return words # Return the resulting list of words

    def __len__(self):
        if self._root is None: # Check whether TST is empty
            return 0
        else:
            return len(self.all_strings()) # Return length of list of all stored strings

    def __repr__(self):
        if self._root is None:
            return 'empty tree'
        else:
            return f'terminates: {self._terminates} \n' + self._root._to_string()


with open('data/search_trees/corncob_lowercase.txt') as file:
    words = [line.strip() for line in file]


import random
import time
sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]


samples = [
    random.sample(words, k=size) for size in sizes
]

nr_runs = 10
times = {}
insert_sample = random.sample(words, k=20)
for sample in samples:
    TST = TernarySearchTree()
    for word in sample:
        TST.insert(word)
    times[len(sample)] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in insert_sample:
            TST.insert(word)
        end_time = time.time_ns()
        times[len(sample)] += end_time - start_time
    times[len(sample)] /= nr_runs*1_000_000.0
print(times)


import matplotlib.pyplot as plt
plt.plot(times.keys(), times.values())
plt.show()
