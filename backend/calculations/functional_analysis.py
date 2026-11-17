# import re
import regex as re

from music21 import harmony, roman, key


def get_roman_numerals(harmonization, setKey):
    if setKey is None:
        tkey = harmonization.analyze('key')
    else:
        tonic, mode = setKey.split()
        tkey = key.Key(tonic, mode)
    roman_numerals = []
    for chord_symbol in harmonization.getElementsByClass(harmony.ChordSymbol):
        roman_numerals.append(roman.romanNumeralFromChord(chord_symbol, tkey).figure)

    return tkey, roman_numerals


# range of [0, 1] given as % values for understandability of users
# 0, if it is not typical
# 1 if it consists entirely of typical progressions / is covered by typical expressions
# combines all matching progressions because they could together cover the whole piece.
# computes extend of coverage with typical progressions.
# returns also a list indicating whether each chord is part of a typical progression
def get_typical_chord_progression_coverage(harmonization_as_roman_numerals, key, chord_durations):
    harmonization_as_roman_numerals_string = " "
    indexes_of_space = [0]
    temp = 0
    for numeral in harmonization_as_roman_numerals:
        harmonization_as_roman_numerals_string += numeral + " "
        # print(numeral)
        temp += len(numeral) + 1
        # print(temp)
        indexes_of_space.append(temp)
    # print("harmonization_as_roman_numerals_string")
    # print(harmonization_as_roman_numerals_string)
    # print("indexes_of_space")
    # print(indexes_of_space)
    coverage_map = [0] * (len(harmonization_as_roman_numerals_string) + 2)
    coverage_map[0] = -1
    coverage_map[len(harmonization_as_roman_numerals_string) - 1] = -1

    # select list based on mode of the estimated key of the piece
    typical_functional_progressions_list = []
    if key.mode == "minor":
        typical_functional_progressions_list = typical_transitions_in_minor_keys
    elif key.mode == "major":
        typical_functional_progressions_list = typical_transitions_in_major_keys
    else:
        typical_functional_progressions_list = typical_functional_progressions

    for typical_progression in typical_functional_progressions_list:
        # print(coverage_map)
        if 0 in coverage_map:
            matches = re.finditer(" " + typical_progression + " ", harmonization_as_roman_numerals_string,
                                  overlapped=True)
            for match in matches:
                # print("match in matches:")
                # print(match)  # print match
                # print(match.start())
                # print(match.end())
                if " " in typical_progression:
                    for i in range(match.start(), match.end()):
                        # print(i)
                        coverage_map[i] = 1
                else:
                    for i in range(match.start(), match.end() + 2):
                        # print(i)
                        coverage_map[i] = 1

        else:
            # print("break")
            break

    coverage_per_chord = []
    coverage_sum = 0
    for i in range(len(indexes_of_space) - 1):
        coverage_map[indexes_of_space[i]] = -1
        coverage_per_chord.append(coverage_map[indexes_of_space[i] + 1])
        coverage_sum += chord_durations[i] * coverage_map[indexes_of_space[i] + 1]
    coverage_map[-1] = -1
    # print("coverage_map")
    # print(coverage_map)

    # print("coverage")
    # print(coverage)
    # print("len(harmonization_as_roman_numerals)")
    # print(len(harmonization_as_roman_numerals))
    coverage = coverage_sum / sum(chord_durations)
    # print("coverage")
    # print(coverage)
    return coverage * 100, coverage_per_chord


# simply a list of typical progressions, given as sequences of roman numerals
# needs a space in between the single roman numerals
typical_functional_progressions = [
    "i VI III VII",
    "I IV V I",
    "IV I",
    "V I"
    "V7 I"
    "I IV V7 I",
]

# list of transitions from paper Isochords by Bergstrom et al.
typical_transitions_in_major_keys = [
    "I",  # any other
    "i",  # any other
    "ii V",
    "ii V7",
    "ii vii",
    "iii ii",
    "iii IV",
    "iii V",
    "iii V7",
    "iii vi",
    "IV I",
    "IV ii",
    "IV V",
    "IV V7",
    "IV vii",
    "V I",
    "V vi",
    "V7 I",
    "V7 vi",
    "vi ii",
    "vi IV",
    "vi V",
    "vi V7",
    "vi iii-IV",
    "vii I"
]

# list of transitions from paper Isochords by Bergstrom et al.
typical_transitions_in_minor_keys = [
    "I",  # any other
    "i",  # any other
    "ii_6 V",
    "ii_6 V7",
    "ii V",
    "ii V7",
    "III ii",
    "III iv",
    "III VI",
    "iv i",
    "iv ii",
    "iv V",
    "iv V7",
    "iv VII",
    "IV V",
    "IV V7",
    "IV vii",
    "V i",
    "V VI",
    "V7 i",
    "V7 VI",
    "v VI",
    "VI ii",
    "VI iv",
    "VI V",
    "VI V7",
    "VI III-iv",
    "vii i",
    "vii VII-III",
    "VII i",
    "VII VII-III"
]
