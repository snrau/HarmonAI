import itertools

from music21 import harmony

from converter import music21_harmonization_to_json


def apply_manipulation_to_harmonization(manipulation_sequence, harmonization):
    # TODO implement
    chords = list(harmonization.flat.getElementsByClass(harmony.ChordSymbol))
    for i in range(len(chords)):
        manipulation_sequence[i](chords[i])

    return harmonization


def inversion0(chord):
    chord.inversion(0)
    chord.closedPosition(inPlace=True, forceOctave=3)


def inversion1(chord):
    chord.inversion(1)
    chord.closedPosition(inPlace=True, forceOctave=3)


def inversion2(chord):
    chord.inversion(2)
    chord.closedPosition(inPlace=True, forceOctave=3)


def generate_variations_within_chords(score, harmonizations_json):
    generated_harmonizations = []

    # TODO somehow solve problem of is triad or how many chord tones
    # TODO how handle different octaves?
    # FIXME the manipulation seems to not reach the bass notes. they remain the previous ones
    chord_tone_manipulation_options = [
        inversion0,  # grundstellung
        inversion1,  # 1. umkehrung
        inversion2  # 2. umkehrung
    ]

    # steps that are needed:

    MAX_VARIATIONS = 27
    MAX_CHANGED_CHORDS = 3

    # loop over all harmonizations
    # (make sure to have the json including attributes that are needed to copy, as well as the music21 version at hand)
    harmonizations = list(score.getElementsByGroup("harmonization"))
    for i in range(len(harmonizations_json)):
        harmonization = harmonizations[i]
        harmonization_json = harmonizations_json[i]

        generated_harmonizations.append(harmonization_json)

        num_chords = len(harmonization_json["chord_symbols"])
        indices = list(range(num_chords))

        variation_count = 0

        # vary only a limited number of chord positions
        for k in range(1, min(MAX_CHANGED_CHORDS + 1, num_chords + 1)):
            for positions in itertools.combinations(indices, k):
                for changes in itertools.product(chord_tone_manipulation_options, repeat=k):

                    # base = original (no change)
                    manipulation_sequence = [inversion0] * num_chords

                    for pos, change in zip(positions, changes):
                        manipulation_sequence[pos] = change

                    # ❌ skip "all inversion0" (= original duplicate)
                    if all(m == inversion0 for m in manipulation_sequence):
                        continue

                    # apply manipulation
                    harmonization_variation = apply_manipulation_to_harmonization(
                        manipulation_sequence,
                        harmonization
                    )

                    # convert to json
                    harmonization_variation_json = music21_harmonization_to_json(
                        harmonization_variation
                    )

                    # copy attributes
                    harmonization_variation_json["AI_Model"] = harmonization_json["AI_Model"]
                    harmonization_variation_json["rythm_density"] = harmonization_json["rythm_density"]

                    # optional but useful
                    harmonization_variation_json["is_variation"] = True
                    harmonization_variation_json["parent_id"] = i

                    generated_harmonizations.append(harmonization_variation_json)

                    variation_count += 1
                    if variation_count >= MAX_VARIATIONS:
                        break
                if variation_count >= MAX_VARIATIONS:
                    break
            if variation_count >= MAX_VARIATIONS:
                break

    return generated_harmonizations


def old_generate_variations_within_chords(score, harmonizations_json):
    generated_harmonizations = []

    # TODO somehow solve problem of is triad or how many chord tones
    # TODO how handle different octaves?
    # FIXME the manipulation seems to not reach the bass notes. they remain the previous ones
    chord_tone_manipulation_options = [
        inversion0,  # grundstellung
        inversion1,  # 1. umkehrung
        inversion2  # 2. umkehrung
    ]

    # steps that are needed:

    # loop over all harmonizations
    # (make sure to have the json including attributes that are needed to copy, as well as the music21 version at hand)
    harmonizations = list(score.getElementsByGroup("harmonization"))
    for i in range(len(harmonizations_json)):
        harmonization = harmonizations[i]
        harmonization_json = harmonizations_json[i]

        generated_harmonizations.append(harmonization_json)
        # compute all combinations of the chord_tone_manipulation_options
        manipulation_sequences = itertools.product(chord_tone_manipulation_options,
                                                   repeat=len(harmonization_json["chord_symbols"]))

        for manipulation_sequence in manipulation_sequences:
            print(manipulation_sequence)
            harmonization_variation = apply_manipulation_to_harmonization(manipulation_sequence, harmonization)

            # convert to json
            harmonization_variation_json = music21_harmonization_to_json(harmonization_variation)

            # join with attributes to copy
            harmonization_variation_json["AI_Model"] = harmonization_json["AI_Model"]
            harmonization_variation_json["rythm_density"] = harmonization_json["rythm_density"]

            # append to generated_harmonizations
            generated_harmonizations.append(harmonization_variation_json)

    return generated_harmonizations
