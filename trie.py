import pickle

class Trie():
    def __init__(self, root={}):
        self.root = root 
        self.end_symbol = "*"

    def add(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                current[letter] = {}
            current = current[letter]
        current[self.end_symbol] = True
    
    def generate_from_words(self, word_list):
        for word in word_list:
            self.add(word)

def save_trie(trie, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(trie, f)

def load_trie(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def get_trie_words(trie_dict, letters, prefix=""):
    words = []
    if trie_dict is None:
        return words
    if "*" in trie_dict.keys():
        words.append(prefix)
    for letter in letters:
        words += get_trie_words(trie_dict.get(letter), letters, prefix + letter)
    return words