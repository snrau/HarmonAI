import { writable } from "svelte/store";

export const music = $state({
    harmonizations: [], /* ... */
    melody: {},
    selected_harmonizations: [],
    selected_harmonizations_indeces: [],
    highlighted_harmonization_index: -1, // -1 resembles non highlighted
    highlighted_harmonization: {}, // the single harmonization itself
    meta: {},
    playing_index: -1,
});

export const selectedIndex = writable(-1);
export const selectedKey = writable("");

// should be 1/32 note duration, based on a quarter note length that is 1.
export const smallest_duration_considered = 0.125


export function process_melody_for_visualization(melody) {
    let processed_melody = [];
    for (let i = 0; i < melody["note_pitches_midi"].length; i++) {
        let number_of_needed_duplicates = melody["note_durations"][i] / smallest_duration_considered;
        for (let j = 0; j < number_of_needed_duplicates; j++) {
            processed_melody.push(melody["note_pitches_midi"][i]);
        }
    }
    return processed_melody;
}


export function process_harmonizations_for_visualization(harmonizations) {
    let processed_harmonizations = [];

    if (harmonizations[0] && harmonizations[0]["key"]) {

        for (let harmonization of harmonizations) {
            let processed_harmonization = {};
            // in the following add attributes that need processing for useful visual representation in lineup

            let MCTD_progression = [];
            let CT_class_progression = [];
            let CT_class_progression_string = [];
            let PCS_progression = [];
            let CT_class_as_numerical_value = {
                "chord_tone": 0,
                "proper_non_chord_tone": 0.5,
                "non_chord_tone": 1,
            }
            // encode durations as well
            // consider each pair of melody tone and corresponding chord, this is not just the number of chords or melody notes
            for (let i = 0; i < harmonization["MCTD_progression"]?.length; i++) {
                let number_of_needed_duplicates = (harmonization["MCTD_progression"][i]["end"] - harmonization["MCTD_progression"][i]["start"]) / smallest_duration_considered;
                for (let j = 0; j < number_of_needed_duplicates; j++) {
                    MCTD_progression.push(harmonization["MCTD_progression"][i]["MCTD"]);
                    CT_class_progression.push(CT_class_as_numerical_value[harmonization["CT_class_progression"][i]["class"]]);
                    CT_class_progression_string.push(harmonization["CT_class_progression"][i]["class"]);
                    PCS_progression.push(harmonization["PCS_progression"][i]["score"]);
                }
            }
            processed_harmonization["MCTD progression (melody tone chord tonal distance)"] = MCTD_progression;
            processed_harmonization["CT class progression (chord tone)"] = CT_class_progression;
            processed_harmonization["CT class progression (chord tone) (string labels)"] = CT_class_progression_string;
            processed_harmonization["PCS progression (pitch consonance score)"] = PCS_progression;

            //reflect chord durations as well
            // oriented on the number of chords in the respective harmonization
            let chords = [];
            let chord_durations = [];
            let bass_notes_midi = [];
            let typicality_of_chords = [];
            let CTDs = [];
            let roman_numerals = [];
            for (let i = 0; i < harmonization["chord_symbols"].length; i++) {
                let number_of_needed_duplicates = harmonization["chord_durations"][i] / smallest_duration_considered;
                for (let j = 0; j < number_of_needed_duplicates; j++) {
                    chords.push(harmonization["chord_symbols"][i]);
                    chord_durations.push(harmonization["chord_durations"][i]);
                    bass_notes_midi.push(harmonization["chords_bass_note_midi"][i]);
                    typicality_of_chords.push(harmonization["typical_chord_progression_coverage_per_chord"][i]);
                    roman_numerals.push(harmonization["roman_numerals"][i]);

                    // if (i !== 0) {
                    //     if (j === 0) {
                    //         CTDs.push(2); // to highlight chord beginnings visually
                    //     } else {
                    //         CTDs.push(harmonization["CTD_per_chord"][i-1]);
                    //     }
                    // } else {
                    //     CTDs.push(NaN);
                    // }
                    if (i !== 0) {
                        let fraction_of_CTD = harmonization["CTD_per_chord"][i - 1] / 4;
                        if (j <= 2) {
                            CTDs.push(harmonization["CTD_per_chord"][i - 1]); // to highlight chord beginnings visually
                        } else if (j === 3) { // decay...
                            CTDs.push(3 * fraction_of_CTD);
                        } else if (j === 4) {
                            CTDs.push(2 * fraction_of_CTD);
                        } else if (j === 5) {
                            CTDs.push(fraction_of_CTD);
                        } else {
                            CTDs.push(0);
                        }
                    } else {
                        CTDs.push(0);
                    }
                }
            }
            processed_harmonization["chords_reflecting_durations"] = chords;
            processed_harmonization["chord_durations_reflecting_durations"] = chord_durations;
            processed_harmonization["chords_bass_note_midi_reflecting_durations"] = bass_notes_midi;
            processed_harmonization["typicality_of_chords_per_chord"] = typicality_of_chords;
            processed_harmonization["CTD per chord (chord tonal distance)"] = CTDs;
            processed_harmonization["roman_numerals_reflecting_durations"] = roman_numerals;

            // keep all data available but implement default selection of columns that seem most useful and others the user can add manually if wanted?
            // ai model specific attributes (as e.g. rhythm density) of harmonizers added in the future could not be considered here, only if all attributes are kept and manual pre-selection of columns is done
            for (let key in harmonization) {
                processed_harmonization[key] = harmonization[key]; // add all attributes unchanged
            }

            processed_harmonizations.push(processed_harmonization);
        }

    }
    //music.harmonizations = processed_harmonizations; // DONT DO THAT, it leads to a probably infinite loop of updating harmonizations
    return processed_harmonizations;

}