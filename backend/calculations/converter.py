import os
from music21 import *



def score_to_musicxml_string(score):
    exporter = musicxml.m21ToXml.GeneralObjectExporter(score)
    xml_bytes = exporter.parse()
    xml_string = xml_bytes.decode("utf-8")
    return xml_string

def json_to_music21(music_json):
    #  build it bottom up:
    # loop through json, create music21 objects from the data items, collect the items in lists, to create next layer
    # of items (e.g. chords from symbols or single notes; measures?, parts, ...

    # convert melody
    melody_json = music_json["melody"]
    part_melody = stream.Part(id="melody")
    for i in range(len(melody_json["note_pitches"])):
        melody_note = note.Note(melody_json["note_pitches"][i])
        melody_note.duration = duration.Duration(melody_json["note_durations"][i])
        part_melody.insert(melody_json["note_starting_times"][i], melody_note)

    # add to score where all musical data is inserted
    score = stream.Score()
    score.insert(0, part_melody)

    # convert harmonizations
    harmonizations_json = music_json["harmonizations"]
    for harmonization_json in harmonizations_json:
        harmonization = stream.Part()
        harmonization.groups.append("harmonization")
        for i in range(len(harmonization_json["note_pitches"])):
            chord_note = note.Note(harmonization_json["note_pitches"][i])
            chord_note.duration = duration.Duration(harmonization_json["note_durations"][i])
            harmonization.insert(harmonization_json["note_starting_times"][i], chord_note)

        for i in range(len(harmonization_json["chord_symbols"])):
            chord_symbol = harmony.ChordSymbol(harmonization_json["chord_symbols"][i])
            chord_symbol.duration = duration.Duration(harmonization_json["chord_durations"][i])
            # ensure that the pitches in the chordsymbols match the specified absolute pitches of the chords
            pitches = []
            for chord_note in harmonization.getElementsByOffset(
                    harmonization_json["chord_starting_times"][i],
                    harmonization_json["chord_starting_times"][i] + harmonization_json["chord_durations"][i],
                    includeEndBoundary=False,
                    mustBeginInSpan=False,
                    mustFinishInSpan=False,
                    includeElementsThatEndAtStart=False
            ).notes:
                pitches.append(chord_note.pitch)
            #     print("ptiches:")
            # print(pitches)
            chord_symbol.pitches = pitches
            harmonization.insert(harmonization_json["chord_starting_times"][i], chord_symbol)

        score.insert(0, harmonization)

    # score.show("text")
    return score

# warning: unfinished (and unused) method!
def music21_to_json(score):
    # TODO implement
    # maybe reuse the json representation and just insert the metrics calculation results?
    # jep, but not here but directly when computing the metrics...

    # no need to convert the melody back since we have that already in needed format

    # convert harmonizations along with the metrics
    harmonizations_json = []
    metrics_json = []
    for harmonization in score.getElementsByGroup("harmonization"):
        chord_symbols = []
        chord_durations = []
        chord_starting_times = []
        note_pitches = []
        note_durations = []
        note_starting_times = []

        for chordSymbol in harmonization.getElementsByClass(harmony.ChordSymbol):
            if chordSymbol.duration != duration.Duration(0.0):
                chord_symbols.append(str(chordSymbol)[29:-1])
                chord_starting_times.append(chordSymbol.offset)
                chord_duration = float(str(chordSymbol.duration)[27:-1])
                chord_durations.append(chord_duration)

                for pitch in chordSymbol.pitches:
                    note_pitches.append(str(pitch))
                    note_durations.append(chord_duration)
                    note_starting_times.append(chordSymbol.offset)

        metadata = harmonization.metadata.all()
        print(metadata)
        # TODO ensure that metrics are ordered?

        harmonization_dict = {
            "chord_symbols": chord_symbols,
            "chord_durations": chord_durations,
            "chord_starting_times": chord_starting_times,
            "note_pitches": note_pitches,
            "note_durations": note_durations,
            "note_starting_times": note_starting_times
        }
        for tuple in metadata:
            if tuple[0] != "software":
                harmonization_dict[tuple[0]] = []
        for tuple in metadata:
            if tuple[0] != "software":
                harmonization_dict[tuple[0]].append(tuple[1])

        harmonizations_json.append(harmonization_dict)

    return {"harmonizations": harmonizations_json, "metrics": metrics_json}


def music21_harmonization_to_json(harmonization):
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


def get_melody_from_mxl(path, filename):
    melody_score = converter.parse(os.path.join(path, filename))

    note_pitches = []
    note_pitches_midi = []
    note_pitch_classes = []
    note_starting_times = []
    note_durations = []

    for melody_note in melody_score.flatten().getElementsByClass(note.Note):
        if melody_note.duration != duration.Duration(0):
            note_pitches.append(str(melody_note.pitch))
            note_pitches_midi.append(melody_note.pitch.midi)
            note_pitch_classes.append(melody_note.pitch.pitchClass)
            note_starting_times.append(melody_note.offset)
            note_duration = float(str(melody_note.duration)[27:-1])
            note_durations.append(note_duration)

    melody = {
        "note_pitches": note_pitches,
        "note_pitches_midi": note_pitches_midi,
        "note_pitch_classes": note_pitch_classes,
        "note_starting_times": note_starting_times,
        "note_durations": note_durations
    }

    return melody
