from scrape import scrape_sbsolver, scrape_full_dict
from trie import Trie, save_trie, load_trie

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

def main():
    while True:
        choice = input("What would like to do? Solve(s)/Update words(u)/Quit(q) ").lower()
        while choice != "s" and choice != "u" and choice != "q":
            choice = input("Please enter 's' to solve or 'u' to update words, or 'q' to quit: ").lower()
        if choice == "s":
            pass
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

main()
