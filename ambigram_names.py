"""Potential ambigram finder.

Takes an input file of names and outputs the ones that are potential good 
ambigrams based on the letter matching map at the top of the file.
"""

import sys

LETTER_MATCHES = {
    "a": {"b", "e", "p", "v"},
    "b": {"a", "e", "g", "q", "u"},
    "c": {"n"},
    "d": {"p"},
    "e": {"a", "b"},
    "f": {"f", "s"},
    "g": {"b", "i"},
    "h": {"u", "y"},
    "i": {"n"},
    "j": {"n", "r"},
    "k": {"k", "x"},
    "l": {"n"},
    "m": {"w"},
    "n": {"c", "i", "j", "l", "t", "v"},
    "o": {"o"},
    "p": {"a", "d"},
    "q": {"b"},
    "r": {"j", "u"},
    "s": {"f", "s"},
    "t": {"n", "t"},
    "u": {"b", "h", "r"},
    "v": {"a", "n"},
    "w": {"m"},
    "x": {"k", "x"},
    "y": {"h"},
    "z": {"z"},
}

def validate_letter_matches():
    """Checks that all data in the LETTER_MATCHES is symmetric."""
    for letter, matches in LETTER_MATCHES.items():
        for match in matches:
            if letter not in LETTER_MATCHES[match]:
                print(f"Letter {letter} in LETTER_MATCHES has a mismatch with {match}")
                return False
    return True


validate_letter_matches()


def could_be_ambigram(name):
    """Returns True if the name could be an ambigram."""
    # TODO: Rewrite with `all(...)`
    for i in range(len(name) // 2 + 1):  # +1 to include middle letter when odd
        if name[i] not in LETTER_MATCHES[name[-(i + 1)]]:
            return False
    return True


def main(input_names_path, output_names_path=None):
    with open(input_names_path, "r") as input_names_file:
        output_names = [
            name for name in input_names_file if could_be_ambigram(name.strip().lower())
        ]
    if output_names_path:
        with open(output_names_path, "w") as output_names_file:
            output_names_file.write("\n".join(output_names))
    else:
        print("\n".join(output_names))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_names_path = sys.argv[1]
        main(input_names_path)
    elif len(sys.argv) == 3:
        input_names_path = sys.argv[1]
        output_names_path = sys.argv[2]
        main(input_names_path, output_names_path)
    else:
        print(
            "Usage: python ambigram_names.py names_list.txt <optional: filtered_names.txt>"
        )
        sys.exit(1)
