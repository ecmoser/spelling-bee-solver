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
    
    def get_dict(self):
        return self.root

    def generate_from_words(self, word_list):
        for word in word_list:
            self.add(word)

def save_trie(trie, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(trie, f)

def load_trie(file_path):
    return pickle.load(file_path)