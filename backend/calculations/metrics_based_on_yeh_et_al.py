"""
Those metrics are based on the descriptions of Yeh et al. in
# TODO add citation

For some I created an additional version that avoids the averaging the intermittent results to obtain
an evolution of the metric throughout the piece since I believe that this is more meaningfull in some contexts
"""
import math
from music21 import *
import numpy as np


# chord histogram entropy and chord coverage
# chord_sequence needs to be a list of music21 harmony.ChordSymbol
# CHE is sum of negative log likelihood of normalized chord probability values
# CHE is lowest (= 0) when only one chord is used in whole piece, entropy is highest when histogram is uniformly distributed
def CHE_and_CC(chord_sequence):
    # initialize histogram
    chord_histogram = {}
    for chord in chord_sequence:
        chord_histogram[chord.figure] = 0

    # directly compute normalized histogram
    for chord in chord_sequence:
        chord_histogram[chord.figure] += 1 / len(chord_sequence)

    # chord coverage is basically the number of chord classes, thus the number of pairs in the histogram dict
    CC = len(chord_histogram)

    # calculate entropy
    # TODO check formula correctness
    CHE = 0
    CHE = sum([CHE + - p_i * np.log(p_i + 1e-6) for p_i in chord_histogram.values()])

    return CHE, CC


# chord tonal distance
# chord_sequence needs to be a list of music21 harmony.ChordSymbol
def CTD(chord_sequence):
    chords_pitch_classes = get_pitch_classes_per_chord(chord_sequence)

    y = 0
    tonal_distances = []
    for n in range(len(chords_pitch_classes) - 1):
        tonal_distance = np.sqrt(
            np.sum((np.asarray(tonal_centroid(chords_pitch_classes[n + 1])) - np.asarray(
                tonal_centroid(chords_pitch_classes[n]))) ** 2))
        y += tonal_distance
        tonal_distances.append(tonal_distance)

    if (len(chords_pitch_classes) - 1) == 0:
        return 0, []

    else:
        return y / (len(chords_pitch_classes) - 1), tonal_distances


# Chord tone to non-chord tone ratio
# harmonization is a music21.stream.Part holding one harmonization as (among other objects) harmony.ChordSymbol
# melody_sequence is the melody as a list of music21.note.Note
#  TODO check whether computes reasonable values... especially the number of proper non chord tones might be wrong calculated
# 1 if there are no non-chord-tones at all
# 1 if all non-chord-tones are also proper-non-chord-tones
# 0 if there are no chord-tones as well as no proper-non-chord-tones = only non-chord-tones
def CTnCTR(melody_sequence, harmonization):
    number_chord_tones = 0
    number_non_chord_tones = 0
    number_proper_non_chord_tones = 0
    CT_classes = []
    for i in range(len(melody_sequence)):
        melody_note = melody_sequence[i]
        corresponding_chords = harmonization.getElementsByOffset(
            offsetStart=melody_note.offset,
            offsetEnd=melody_note.offset + float(str(melody_note.duration)[27:-1]),
            includeEndBoundary=False,
            mustBeginInSpan=False,
            mustFinishInSpan=False,
            includeElementsThatEndAtStart=False
        ).getElementsByClass(harmony.ChordSymbol)
        for chord in corresponding_chords:
            CT_class = {}
            CT_class["start"] = max(melody_note.offset, chord.offset)
            CT_class["end"] = min(melody_note.offset + float(str(melody_note.duration)[27:-1]),
                                  chord.offset + float(str(chord.duration)[27:-1]))
            if melody_note.pitch.pitchClass in chord.pitchClasses:
                number_chord_tones += 1
                CT_class["class"] = "chord_tone"
            else:
                number_non_chord_tones += 1
                CT_class["class"] = "non_chord_tone"
                # iterate over all melody tones that follow the one currently examined
                for j in range(i, len(melody_sequence)):
                    # if examined one and following one are not the same
                    if melody_note.pitch.pitchClass != melody_sequence[j].pitch.pitchClass:
                        # if following one is a chord tone AND absolute of the difference of the pitchclasses of the
                        # tones is 2 at max (= within two semitones )
                        # proper in the sense of it is an accepted non-chord-tone because it is well selected in musical context
                        if (melody_sequence[j].pitch.pitchClass in chord.pitchClasses and
                                interval.Interval(melody_sequence[j], melody_note).semitones <= 2):
                            number_proper_non_chord_tones += 1
                            CT_class["class"] = "proper_non_chord_tone"
                        break
            CT_classes.append(CT_class)

    # after counting is done:
    if (number_chord_tones + number_non_chord_tones) == 0:
        return 0
    return (number_chord_tones + number_proper_non_chord_tones) / (
            number_chord_tones + number_non_chord_tones), CT_classes


# Pitch consonance score
# harmonization is a music21.stream.Part holding one harmonization as (among other objects) harmony.ChordSymbol
# melody_sequence is the melody as a list of music21.note.Note
#  normalized range: [-1, 1] negative is dissonant, positive consonant
def PCS(melody_sequence, harmonization):
    score_progression = []
    score_sum = 0
    count = 0

    for i in range(len(melody_sequence)):
        melody_note = melody_sequence[i]
        corresponding_chords = harmonization.getElementsByOffset(
            offsetStart=melody_note.offset,
            offsetEnd=melody_note.offset + float(str(melody_note.duration)[27:-1]),
            includeEndBoundary=False,
            mustBeginInSpan=False,
            mustFinishInSpan=False,
            includeElementsThatEndAtStart=False
        ).getElementsByClass(harmony.ChordSymbol)
        for chord in corresponding_chords:
            score = {}
            score["start"] = max(melody_note.offset, chord.offset)
            score["end"] = min(melody_note.offset + float(str(melody_note.duration)[27:-1]),
                               chord.offset + float(str(chord.duration)[27:-1]))
            score["score"] = 0

            for chord_pitch in chord.pitches:
                interval_to_test = interval.Interval(pitchStart=chord_pitch, pitchEnd=melody_note)
                if interval_to_test.isConsonant():
                    # unison, maj, minor 3rd, perfect 5th, maj, minor 6
                    count += 1
                    score["score"] += 1 / (len(chord.pitches))
                    score_sum += 1
                elif interval_to_test.simpleName == "p4":
                    # perfect 4th
                    count += 1
                else:
                    # dissonant interval
                    count += 1
                    score["score"] += -1 / (len(chord.pitches))
                    score_sum += -1

            score_progression.append(score)
    if count == 0:
        return 0, []
    return score_sum / count, score_progression


# melody_sequence-chord tonal distance

# harmonization is a music21.stream.Part holding one harmonization as (among other objects) harmony.ChordSymbol
# melody_sequence is the melody as a list of music21.note.Note
# TODO what is melody sequence needing as input format?
def MCTD(melody_sequence, harmonization):
    MCTD_progression = []
    MCTD_sum = 0

    for i in range(len(melody_sequence)):
        melody_note = melody_sequence[i]
        corresponding_chords = harmonization.getElementsByOffset(
            offsetStart=melody_note.offset,
            offsetEnd=melody_note.offset + float(str(melody_note.duration)[27:-1]),
            includeEndBoundary=False,
            mustBeginInSpan=False,
            mustFinishInSpan=False,
            includeElementsThatEndAtStart=False
        ).getElementsByClass(harmony.ChordSymbol)
        for chord in corresponding_chords:
            tonal_distance = {}
            tonal_distance["start"] = max(melody_note.offset, chord.offset)
            tonal_distance["end"] = min(melody_note.offset + float(str(melody_note.duration)[27:-1]),
                                        chord.offset + float(str(chord.duration)[27:-1]))
            # compute tonal distance
            tonal_distance["MCTD"] = np.sqrt(
                np.sum(
                    (np.asarray(tonal_centroid([melody_note.pitch.pitchClass]))
                     - np.asarray(tonal_centroid(chord.pitchClasses))) ** 2
                )
            )
            # for the sum weight tonal distance by duration of pair of melody note and chord are sounding simultaneously
            MCTD_sum += tonal_distance["MCTD"] * (tonal_distance["end"] - tonal_distance["start"])

            MCTD_progression.append(tonal_distance)

    if harmonization.duration == duration.Duration(0):
        return 0, []
    return MCTD_sum / float(str(harmonization.duration)[27:-1]), MCTD_progression


# chord_sequence needs to be a list of music21 harmony.ChordSymbol
# pitch classes are given as numbers 0 to 11, where C=0, C#=1, D=2, etc. to B=11
def get_pitch_classes_per_chord(chord_sequence):
    chords_pitch_classes = []
    for chord in chord_sequence:
        chords_pitch_classes.append(chord.pitchClasses)
    return chords_pitch_classes


# Calculate tonal coordinate in tonal space
def tonal_centroid(notes):
    fifths_lookup = {9: [1.0, 0.0], 2: [math.cos(math.pi / 6.0), math.sin(math.pi / 6.0)],
                     7: [math.cos(2.0 * math.pi / 6.0), math.sin(2.0 * math.pi / 6.0)],
                     0: [0.0, 1.0], 5: [math.cos(4.0 * math.pi / 6.0), math.sin(4.0 * math.pi / 6.0)],
                     10: [math.cos(5.0 * math.pi / 6.0), math.sin(5.0 * math.pi / 6.0)],
                     3: [-1.0, 0.0], 8: [math.cos(7.0 * math.pi / 6.0), math.sin(7.0 * math.pi / 6.0)],
                     1: [math.cos(8.0 * math.pi / 6.0), math.sin(8.0 * math.pi / 6.0)],
                     6: [0.0, -1.0], 11: [math.cos(10.0 * math.pi / 6.0), math.sin(10.0 * math.pi / 6.0)],
                     4: [math.cos(11.0 * math.pi / 6.0), math.sin(11.0 * math.pi / 6.0)]}
    minor_thirds_lookup = {3: [1.0, 0.0], 7: [1.0, 0.0], 11: [1.0, 0.0],
                           0: [0.0, 1.0], 4: [0.0, 1.0], 8: [0.0, 1.0],
                           1: [-1.0, 0.0], 5: [-1.0, 0.0], 9: [-1.0, 0.0],
                           2: [0.0, -1.0], 6: [0.0, -1.0], 10: [0.0, -1.0]}
    major_thirds_lookup = {0: [0.0, 1.0], 3: [0.0, 1.0], 6: [0.0, 1.0], 9: [0.0, 1.0],
                           2: [math.cos(7.0 * math.pi / 6.0), math.sin(7.0 * math.pi / 6.0)],
                           5: [math.cos(7.0 * math.pi / 6.0), math.sin(7.0 * math.pi / 6.0)],
                           8: [math.cos(7.0 * math.pi / 6.0), math.sin(7.0 * math.pi / 6.0)],
                           11: [math.cos(7.0 * math.pi / 6.0), math.sin(7.0 * math.pi / 6.0)],
                           1: [math.cos(11.0 * math.pi / 6.0), math.sin(11.0 * math.pi / 6.0)],
                           4: [math.cos(11.0 * math.pi / 6.0), math.sin(11.0 * math.pi / 6.0)],
                           7: [math.cos(11.0 * math.pi / 6.0), math.sin(11.0 * math.pi / 6.0)],
                           10: [math.cos(11.0 * math.pi / 6.0), math.sin(11.0 * math.pi / 6.0)]}

    fifths = [0.0, 0.0]
    minor = [0.0, 0.0]
    major = [0.0, 0.0]
    r1 = 1
    r2 = 1
    r3 = 0.5
    if notes:
        for note in notes:
            for i in range(2):
                fifths[i] += r1 * fifths_lookup[note][i]
                minor[i] += r2 * minor_thirds_lookup[note][i]
                major[i] += r3 * major_thirds_lookup[note][i]
        for i in range(2):
            fifths[i] /= len(notes)
            minor[i] /= len(notes)
            major[i] /= len(notes)

    return fifths + minor + major
