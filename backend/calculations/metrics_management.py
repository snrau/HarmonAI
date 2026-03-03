from functional_analysis import get_roman_numerals, get_typical_chord_progression_coverage
from metrics_based_on_yeh_et_al import CHE_and_CC, CTD, CTnCTR, PCS, MCTD
from music21 import *

def harmonization_to_midi_events(harmonization, melody):
    events = []


    if not isinstance(harmonization, stream.Stream):
        harmonization_stream = stream.Stream(harmonization)
    else:
        harmonization_stream = harmonization
    # --- 1. Add harmonization (chords) ---
    for n in harmonization_stream.notes:  # flatten to get all notes in the stream
        start = float(n.offset)
        duration = float(n.quarterLength)
        end = start + duration

        if isinstance(n, note.Note):
            events.append({
                "pitch": n.pitch.midi,
                "startTime": start,
                "endTime": end,
            })
        elif isinstance(n, chord.Chord):
            for p in n.pitches:
                events.append({
                    "pitch": p.midi,
                    "startTime": start,
                    "endTime": end,
                })

    if not isinstance(melody, stream.Stream):
        melody_stream = stream.Stream(melody)
    else:
        melody_stream = melody

    # --- 2. Add melody from music21 stream ---
    for n in melody_stream.notes:  # flatten to get all notes in the stream
        start = float(n.offset)
        duration = float(n.quarterLength)
        end = start + duration

        if isinstance(n, note.Note):
            events.append({
                "pitch": n.pitch.midi,
                "startTime": start,
                "endTime": end,
            })
        elif isinstance(n, chord.Chord):
            for p in n.pitches:
                events.append({
                    "pitch": p.midi,
                    "startTime": start,
                    "endTime": end,
                })

    # --- 3. Sort by startTime (important for playback) ---
    events.sort(key=lambda e: e["startTime"])

    return events

def calculate_metrics(score, harmonizations_json):
    # kind of register here all different metrics that can be calculated?

    harmonizations = list(score.getElementsByGroup("harmonization"))

    melody = list(score.getElementById("melody").recurse().notes)
    # print("melody:")
    # # melody.show("text")
    # print(melody)

    for i in range(len(harmonizations_json)):
        harmonization = harmonizations[i]

        chord_names = []
        chord_symbols = []
        chord_durations = []
        bass_notes = []
        bass_notes_midi = []
        for chord_symbol in harmonization.getElementsByClass(harmony.ChordSymbol):
            if chord_symbol.duration != duration.Duration(0.0):
                chord_names.append(chord_symbol.figure)
                chord_symbols.append(chord_symbol)
                chord_duration = float(str(chord_symbol.duration)[27:-1])
                chord_durations.append(chord_duration)

                bass_notes.append(str(chord_symbol.bass()))
                bass_notes_midi.append(chord_symbol.bass().midi)

        harmonizations_json[i]["chords_bass_note"] = bass_notes
        harmonizations_json[i]["chords_bass_note_midi"] = bass_notes_midi

        harmonizations_json[i]["midiplayback"] = harmonization_to_midi_events(harmonization, melody)

        # compute and save some metrics
        # save all metrics results alongside the respective harmonization, since the melody is for all the same
        # in particular also results that may belong more to the melody are kept here anyways
        harmonizations_json[i]["CHE"], harmonizations_json[i]["CC"] = CHE_and_CC(chord_symbols)
        harmonizations_json[i]["CTD_average"], harmonizations_json[i]["CTD_per_chord"] = CTD(chord_symbols)

        harmonizations_json[i]["CTnCTR"], harmonizations_json[i]["CT_class_progression"] = CTnCTR(melody, harmonization)
        harmonizations_json[i]["PCS"], harmonizations_json[i]["PCS_progression"] = PCS(melody, harmonization)
        harmonizations_json[i]["MCTD_average"], harmonizations_json[i]["MCTD_progression"] = MCTD(melody, harmonization)

        # functional analysis
        key, roman_numerals = get_roman_numerals(harmonization)
        harmonizations_json[i]["key"] = str(key)
        harmonizations_json[i]["roman_numerals"] = roman_numerals
        harmonizations_json[i]["typical_chord_progression_coverage"], harmonizations_json[i][
            "typical_chord_progression_coverage_per_chord"] = get_typical_chord_progression_coverage(roman_numerals,
                                                                                                     key,
                                                                                                     chord_durations)

    # print(harmonizations_json)
    # harmonizations.show("text")
    # score.show("text")
    return harmonizations_json


def get_note_ranges(score):
    earliest_start = score.lowestOffset
    latest_end = earliest_start + score.duration.quarterLength

    # initialise with min/max possible midi values
    min_pitch = 127
    max_pitch = 0

    for harmonization in score.getElementsByGroup("harmonization"):
        for harmony_note in harmonization.flatten().getElementsByClass(note.Note):
            min_pitch = min(min_pitch, harmony_note.pitch.midi)
            max_pitch = max(max_pitch, harmony_note.pitch.midi)

    min_x = earliest_start
    min_y = -1 * max_pitch
    min_width = latest_end - earliest_start
    min_height = abs(min_y - (-1 * min_pitch)) + 1

    viewbox = str(int(min_x)) + " " + str(int(min_y)) + " " + str(int(min_width)) + " " + str(int(min_height))

    return {"earliest_start": earliest_start, "latest_end": latest_end, "min_pitch": min_pitch, "max_pitch": max_pitch, "viewbox_harmonizations": viewbox}
