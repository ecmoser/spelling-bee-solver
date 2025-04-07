from scrape import scrape_sbsolver, scrape_full_dict
from trie import Trie, save_trie, load_trie, get_trie_words
from prettyify import matches_string

def update_used_words():
    used_trie = Trie()
    with open("dicts/used_words.txt", "w") as f:
        for letter in "abcdefghijklmnopqrstuvwxyz":
            url = f"https://sbsolver.com/lexicon/{letter}"
            for word in scrape_sbsolver(url):
                f.write(word.lower() + "\n")
                used_trie.add(word.lower())
        f.close()
    save_trie(used_trie, "dicts/used_words_trie.pkl")

def update_full_dictionary():
    full_trie = Trie()
    with open("dicts/full_dictionary.txt", "w") as f:
        url = "https://gist.githubusercontent.com/deostroll/7693b6f3d48b44a89ee5f57bf750bd32/raw/426f564cf73b4c87d2b2c46ccded8a5b98658ce1/dictionary.txt"
        for word in scrape_full_dict(url):
            if len(word) > 3:
                f.write(word.lower() + "\n")
                full_trie.add(word.lower())
        f.close()
    save_trie(full_trie, "dicts/full_dictionary_trie.pkl")

def solve_puzzle(puzzle):
    used_trie = load_trie("dicts/used_words_trie.pkl")
    full_trie = load_trie("dicts/full_dictionary_trie.pkl")
    letters = [letter.lower() for letter in puzzle]
    center_letter = ''
    for letter in puzzle:
        if letter.isupper():
            center_letter = letter.lower()
    used_word_matches = []
    full_word_matches = []
    pangrams = []
    for word in get_trie_words(used_trie, letters):
        if center_letter in word:
            all_letters = True
            for letter in letters:
                if letter not in word:
                    all_letters = False
            if all_letters:
                pangrams.append(word)
            else:
                used_word_matches.append(word)
    for word in get_trie_words(full_trie, letters):
        if center_letter in word:
            all_letters = True
            for letter in letters:
                if letter not in word:
                    all_letters = False
            if all_letters:
                pangrams.append(word)
            else:
                full_word_matches.append(word)
    return matches_string(used_word_matches, full_word_matches, pangrams)
                

def main():
    while True:
        choice = input("What would like to do? Solve(s)/Update words(u)/Quit(q) ").lower()
        while choice != "s" and choice != "u" and choice != "q" and choice != "test":
            choice = input("Please enter 's' to solve or 'u' to update words, or 'q' to quit: ").lower()
        if choice == "s":
            puzzle = input("Enter the puzzle with the center letter capitalized: ")
            caps = 0
            for letter in puzzle:
                if letter.isupper():
                    caps += 1
            while len(puzzle) != 7 or caps != 1:
                puzzle = input("Please enter a 7-letter puzzle in the format abcDefg: ")
                caps = 0
                for letter in puzzle:
                    if letter.isupper():
                        caps += 1
        elif choice == "u":
            choice = input("Update used words(u) or full dictionary(f)? ").lower()
            while choice != "u" and choice != "f":
                choice = input("Please enter 'u' to update used words or 'f' for full dictionary: ").lower()
            if choice == "u":
                print("This will take a while...")
                update_used_words()
            elif choice == "f":
                update_full_dictionary()
        elif choice == "q":
            print("Quitting!")
            return
        elif choice == "test":
            print(len("previously used words"))
            print(matches_string(["a", "b", "c"], ["d", "e"], ["g", "h", "i"]))

main()
