from itertools import zip_longest

def matches_string(used_words, full_words, pangrams):
    used_words.sort()
    full_words.sort()
    pangrams.sort()
    num_used = len(used_words)
    num_pangram = len(pangrams)
    num_full = len(full_words)
    points_used = sum([len(word) if len(word) > 4 else 1 for word in used_words])
    points_pangram = sum([len(word) + 7 if len(word) > 4 else 8 for word in pangrams])
    points_full = sum([len(word) if len(word) > 4 else 1 for word in full_words])
    longest_used = max(len(word) for word in used_words) if len(used_words) > 0 else 0
    longest_pangram = max(len(word) for word in pangrams) if len(pangrams) > 0 else 0
    longest_title = len(f"Previously Used Words ({num_used})")
    longest_word = int(max(longest_used, longest_pangram, longest_title))
    result = f"Total words: {num_used + num_pangram + num_full} ({points_used + points_pangram + points_full} points)\n"
    result += f"Used Words: {num_used + num_pangram} ({points_used + points_pangram} points)\n"
    result += f"{f'Previously Used Words ({num_used})':<{longest_word}} | {f'Pangrams ({num_pangram})':<{longest_word}} | {f'Remaining Words ({num_full})'}\n"
    result += ''.join(['-' * longest_word + ' | ' + '-' * longest_word + ' | ' + '-' * longest_word + '\n'])
    for used, pangram, full in zip_longest(used_words, pangrams, full_words, fillvalue=''):
        result += f"{used:<{longest_word}} | {pangram:<{longest_word}} | {full}\n"
    print(result)
    return result
