# Solver for the NYT Spelling Bee

## What is this project?

### The Game
The [New York Times Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) game is a game where you are given seven letters with one in the middle, and your job is to find words of at least 4 letters in length that use only those letters, and must use the center letter. However, for someone with a limited vocabulary this can be difficult and embarassing. That's why I made a program to find all possible words in a puzzle so that you can show off your perfect scores to your friends.

### The Solution
The program scrapes online databases of words that have previously been used in the game, as well as the full dictionary, to get a comprehensive list of words that may be used. Not all words that satisfy the conditions, however, are accepted by the game as there is an editor that removes words he considers to be offensive or too obscure to be fun. Because of this, the program splits its output into words that have been used before and those which have not, which are less likely to appear as a solution.

### The Process
After the words have been scraped, they are inserted into a dictionary formatted as a data structure called a trie, with each letter in the word being a point. This allows for a much more efficient search of the list of words as we only check branches of the trie that contain valid letters, and we can quickly exclude most possible words. The program does this twice, once for the full dictionary and once for the dicionary of previously used words, and stores the outputs to a list which it then formats and prints. It also checks if words are pangrams, a special solution containing all letters in the puzzle, and displays them seperately.

## How to use

### Setup
If you are unfamiliar with how to use git, go somewhere else and learn before coming back.
1. Clone this repo into a local directory on your pc and open a command prompt in that directory.
2. Create a virtual environment by running `python3 -m venv venv`. If you dont have pytyhon3 installed, install it as well as the python3.12-venv package before doing this.
3. Activate the virtual environment by running `.\venv\bin\activate` on windows or `source venv/bin/activate` on Mac or Unix.
4. Once in the virtual environment, install dependencies using `pip install -r requirements.txt`.
5. Run `playwright install`  and then `playwright install-deps` to install browsers for playwright. This is what is used for scraping online databases.
6. To run the program, run `python3 main.py` in the virtual environment.
7. (Optional) When done using the script, run `deactivate` to stop the virtual environment

### Program Usage
1. On the first time running the program or any subsequent time which you would like to update the word list, enter "u" for update and then "b" for both to update both the list of previously used words and the list of all words in the English dictionary. This will take a while, so be patient. On future uses, you also have the option to update each of the lists individually or skip this step entirely.
2. Enter "s" to solve a puzzle, then enter the puzzle you would like solved. It must be a string of 7 letters with only 1 capitalized, the capitalized letter being the center letter in the puzzle that must be used in all words. (Ex. aeFrtsi)
3. View your solved puzzle.
4. If you would like to solve another puzzle, repeat step 2. Otherwise, enter "q" to quit the program.

## Future Improvements
- **Basic GUI:** Add a user interface to make the program more usable by casual users. (IN PROGRESS)
- **Faster Fetching:** Improve speed at which program retrieves dictionaries.
