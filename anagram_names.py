"""Find all sets of anagrams from a list of names.


Usage: python anagram_names.py names_list.txt <optional: output_names.txt>
"""

import sys


def find_one_name_anagrams(names) -> list[list[str]]:
    """Returns all sets of anagrams from the names."""
    anagrams = dict()
    anagrams.setdefault
    for name in names:
        key = str(sorted(name.lower()))
        anagrams.setdefault(key, []).append(name)
    return [v for v in anagrams.values() if len(v) > 1]


def report(anagrams):
    """Prints the largest sets of anagrams and then all, long to short."""
    largest_sets = sorted(
        [a for a in anagrams if len(a) > 2], key=lambda x: len(x), reverse=True
    )
    print("The largest sets of anagrams are:")
    for name_set in largest_sets:
        print(" ".join(name_set))

    print("\nAll anagrams")
    longest_names = sorted(anagrams, key=lambda x: len(x[0]), reverse=True)
    for name_set in longest_names[:50]:
        print(" ".join(name_set))


def main(input_names_path):
    with open(input_names_path, "r") as input_names_file:
        input_names = [name.strip() for name in input_names_file]
    one_name_anagrams = find_one_name_anagrams(input_names)
    report(one_name_anagrams)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_names_path = sys.argv[1]
        main(input_names_path)
    else:
        print("Usage: python ambigram_names.py names_list.txt")
        sys.exit(1)
