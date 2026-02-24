import json
import os.path

from music21 import *

from config import OUTPUTS_PATH, INPUTS_PATH
from loader import get_filenames


def mxl_to_dict(filename):
    harmonization = converter.parse(filename)
    harmony.realizeChordSymbolDurations(harmonization)

    chord_symbols = []
    chord_durations = []
    chord_starting_times = []
    note_pitches = []
    note_durations = []
    note_starting_times = []
    note_pitch_classes = []
    note_pitches_midi = []
    for chordSymbol in harmonization.flat.getElementsByClass(harmony.ChordSymbol):
        if chordSymbol.duration != duration.Duration(0.0):
            chord_symbols.append(str(chordSymbol)[29:-1])
            chord_starting_times.append(chordSymbol.offset)
            chord_duration = float(str(chordSymbol.duration)[27:-1])
            chord_durations.append(chord_duration)

            for pitch in chordSymbol.pitches:
                note_pitches.append(str(pitch))
                note_durations.append(chord_duration)
                note_starting_times.append(chordSymbol.offset)
                # integer value for the pitch, 0-11, where C=0, C#=1, D=2, etc. to B=11
                note_pitch_classes.append(pitch.pitchClass)
                # Midi values are constrained to the space 0-127. Higher or lower values will be transposed octaves to fit in this space.
                note_pitches_midi.append(pitch.midi)

    harmonization_dict = {
        "chord_symbols": chord_symbols,
        "chord_durations": chord_durations,
        "chord_starting_times": chord_starting_times,
        "note_pitches": note_pitches,
        "note_durations": note_durations,
        "note_starting_times": note_starting_times,
        "note_pitch_classes": note_pitch_classes,
        "note_pitches_midi": note_pitches_midi
    }
    return harmonization_dict


def construct_harmonies_table(filenames):
    harmonies_table = []
    for filename in filenames:
        harmonization_dict = mxl_to_dict(filename)
        harmonization_dict["AI_Model"] = "AutoHarmonizer"
        harmonization_dict["rythm_density"] = float(filename.split("_")[-1][0:-4])
        harmonies_table.append(harmonization_dict)

    return harmonies_table


def json_to_music21(melody_json):
    # convert melody
    part_melody = stream.Part(id="melody")
    for i in range(len(melody_json["note_pitches"])):
        melody_note = note.Note(melody_json["note_pitches"][i])
        melody_note.duration = duration.Duration(melody_json["note_durations"][i])
        part_melody.insert(melody_json["note_starting_times"][i], melody_note)

    # add to a score to properly manage musical data
    score = stream.Score()
    score.insert(0, part_melody)
    return score


def provide_as_model_input(melody_json):
    melody = json_to_music21(melody_json)
    melody.write('mxl', fp=os.path.join(INPUTS_PATH, "input_melody.mxl"))


if __name__ == '__main__':
    test = construct_harmonies_table(get_filenames(input_dir=OUTPUTS_PATH))
    print(test)
    # test.show('text')
    # test2 = test.chordify()
    # test2.show()
