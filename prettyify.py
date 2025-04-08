from itertools import zip_longest

def matches_string(used_words, full_words, pangrams):
    used_words.sort()
    full_words.sort()
    pangrams.sort()
    longest_used = max(len(word) for word in used_words) if len(used_words) > 0 else 0
    longest_pangram = max(len(word) for word in pangrams) if len(pangrams) > 0 else 0
    longest_title = len("Previously Used Words")
    longest_word = int(max(longest_used, longest_pangram, longest_title))
    result = f"{'Previously Used Words':<{longest_word}} | {'Pangrams':<{longest_word}} | {'Remaining Words'}\n"
    result += ''.join(['-' * longest_word + ' | ' + '-' * longest_word + ' | ' + '-' * longest_word + '\n'])
    for used, pangram, full in zip_longest(used_words, pangrams, full_words, fillvalue=''):
        result += f"{used:<{longest_word}} | {pangram:<{longest_word}} | {full}\n"
    print(result)
    return result
