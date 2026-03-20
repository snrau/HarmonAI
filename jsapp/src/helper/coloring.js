import {
    music,
    process_harmonizations_for_visualization,
    smallest_duration_considered,
} from "../state.svelte.js";
import * as d3 from "d3";


const phase12 = [
    "#3b4cc0",
    "#5a78d6",
    "#6fa6e8",
    "#7fcdbb",
    "#90d743",
    "#c7e11e",
    "#f1e51d",
    "#fdb42f",
    "#f8765c",
    "#e84a8a",
    "#b536b2",
    "#6a3d9a"
];

const phaseInterpolate = d3.interpolateRgbBasis([
    "#3b4cc0",
    "#6fa6e8",
    "#7fcdbb",
    "#c7e11e",
    "#fdb42f",
    "#f8765c",
    "#b536b2",
    "#3b4cc0" // wichtig: zyklisch schließen!
]);


export function get_color_for_metric(metric, notes_harmonization, number_of_smallest_units_in_piece) {
    let colors = [];
    if (metric === "pitch_class_melody") {
        for (let i = 0; i < number_of_smallest_units_in_piece; ++i) {
            colors.push(
                getPitchClassColor(
                    music.melody["note_pitches_midi_reflecting_durations"][
                    i
                    ] % 12,
                ),
            );
        }
    }
    if (metric === "PCS") {
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            notes_harmonization["PCS progression (pitch consonance score)"]
                .length;
            ++i
        ) {
            colors.push(
                getPCSColor(
                    notes_harmonization[
                    "PCS progression (pitch consonance score)"
                    ][i],
                ),
            );
        }
    }
    if (metric === "MCTD") {
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            notes_harmonization[
                "MCTD progression (melody tone chord tonal distance)"
            ].length;
            ++i
        ) {
            colors.push(
                get_MCTD_Color(
                    notes_harmonization[
                    "MCTD progression (melody tone chord tonal distance)"
                    ][i],
                ),
            );
        }
    }
    if (metric === "CT_class") {
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            notes_harmonization[
                "CT class progression (chord tone) (string labels)"
            ].length;
            ++i
        ) {
            colors.push(
                get_CT_class_Color(
                    notes_harmonization[
                    "CT class progression (chord tone) (string labels)"
                    ][i],
                ),
            );
        }
    }
    if (metric === "CT_class_prog") {
        const prog = Object.values(notes_harmonization[
            "CT_class_progression"
        ])
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            prog.length;
            ++i
        ) {
            colors.push(
                get_CT_class_Color(
                    prog[i].class,
                ),
            );
        }
    }
    if (metric === "typicality_of_chords") {
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            notes_harmonization["typicality_of_chords_per_chord"].length;
            ++i
        ) {
            colors.push(
                get_typicality_of_chords_Color(
                    notes_harmonization["typicality_of_chords_per_chord"][
                    i
                    ],
                ),
            );
        }
    }
    if (metric === "CTD") {
        // here always work on the harmonization attributes, since there are the computed metrics saved
        for (
            let i = 0;
            i <
            notes_harmonization["CTD per chord (chord tonal distance)"]
                .length;
            ++i
        ) {
            colors.push(
                get_CTD_Color(
                    notes_harmonization[
                    "CTD per chord (chord tonal distance)"
                    ][i],
                ),
            );
        }
    }
    return colors;
}

function getPCSColor(PCS_value) {
    return d3.scaleLinear(
        [-1, 0, 1],
        ["darkred", "white", "darkblue"],
    )(PCS_value);
}

function get_MCTD_Color(value) {
    return d3.scaleLinear([0, 3], ["white", "darkviolet"])(value);
}

function get_CT_class_Color(label) {
    if (label === "chord_tone") {
        return "darkblue";
    } else if (label === "proper_non_chord_tone") {
        return "darkorange";
    } else if (label === "non_chord_tone") {
        return "darkred";
    }
    return "white";
}

export function get_typicality_of_chords_Color(value) {
    // TODO check grey values
    if (value === 0) {
        return "#aaa";
    } else if (value === 1) {
        return "darkcyan";
    }
}

function get_CTD_Color(value) {
    return d3.scaleLinear([0, 2], ["#ccc", "darkblue"]).unknown("white")(
        value,
    );
}

export function getPitchClassColor(pitchclass, color_palette = "meaningful_fifths") {
    // TODO select useful coloring
    // rainbow
    // black white as piano tastatur
    // helle farben weiße tasten, dunkle farben schwarze tasten
    // circle of ... fifths/thirds/... or other ideas from literature

    if (color_palette.includes("meaningful")) {
        if (color_palette === "meaningful_fifths") {
            return cyclicHarmonicColoring(pitchclass, "fifths");
        } else if (color_palette === "meaningful_thirds") {
            return cyclicHarmonicColoring(pitchclass, "thirds");
        } else if (color_palette === "meaningful_folded") {
            return cyclicHarmonicColoring(pitchclass, "fifthsFolded");
        } else {
            return cyclicHarmonicColoring(pitchclass, "fifthsFoldedOther");
        }
    }

    // integer value for the pitch, 0-11, where C=0, C#=1, D=2, etc. to B=11
    let color_mapping = {
        rainbow: {
            0: "red", // C
            1: "darkorange", // C#, Db
            2: "#ffdf3f", // D ffdf3f
            3: "#b2d55f", // D#, Eb
            4: "green", // E, Fb
            5: "turquoise", // F, E#
            6: "#1f97ff", // F#, Gb  "#1f78b4"
            7: "blue", // G
            8: "darkblue", // G#, Ab
            9: "darkviolet", // A
            10: "violet", // A#, Bb
            11: "darkred", // B
        },
        rainbow_circle_fifths: {
            0: "red", // C
            7: "darkorange", // G
            2: "#ffdf3f", // D ffdf3f
            9: "#b2d55f", // A
            4: "green", // E, Fb
            11: "turquoise", // B
            6: "#1f97ff", // F#, Gb  "#1f78b4"
            1: "blue", // C#, Db
            8: "darkblue", // G#, Ab
            3: "darkviolet", // D#, Eb
            10: "violet", // A#, Bb
            5: "darkred", // F, E#
        },

        set3_12_class: {
            0: "#8dd3c7", // C
            1: "#ffffb3", // C#, Db
            2: "#bebada", // D
            3: "#fb8072", // D#, Eb
            4: "#80b1d3", // E, Fb
            5: "#fdb462", // F, E#
            6: "#b3de69", // F#, Gb
            7: "#fccde5", // G
            8: "#d9d9d9", // G#, Ab
            9: "#bc80bd", // A
            10: "#ccebc5", // A#, Bb
            11: "#ffed6f", // B
        },

        paired_12_class: {
            0: "#a6cee3", // C
            1: "#1f78b4", // C#, Db
            2: "#b2df8a", // D
            3: "#33a02c", // D#, Eb
            4: "#fb9a99", // E, Fb
            5: "#e31a1c", // F, E#
            6: "#fdbf6f", // F#, Gb
            7: "#ff7f00", // G
            8: "#cab2d6", // G#, Ab
            9: "#6a3d9a", // A
            10: "#ffff99", // A#, Bb
            11: "#b15928", // B
        },

        paired_12_class_rainbow: {
            0: "#e31a1c", // C
            1: "#fb9a99", // C#, Db
            2: "#ff7f00", // D
            3: "#b15928", // D#, Eb
            4: "#fdbf6f", // E, Fb
            5: "#ffff99", // F, E#
            6: "#b2df8a", // F#, Gb
            7: "#33a02c", // G
            8: "#1f78b4", // G#, Ab
            9: "#a6cee3", // A
            10: "#6a3d9a", // A#, Bb
            11: "#cab2d6", // B
        },

        black_and_white: {
            0: "lightgrey", // C
            1: "black", // C#, Db
            2: "lightgrey", // D
            3: "black", // D#, Eb
            4: "lightgrey", // E, Fb
            5: "lightgrey", // F, E#
            6: "black", // F#, Gb
            7: "lightgrey", // G
            8: "black", // G#, Ab
            9: "lightgrey", // A
            10: "black", // A#, Bb
            11: "lightgrey", // B
        },
    };
    return color_mapping[color_palette][pitchclass];
}

const bToSharpMap = {
    "Db": "C#",
    "Eb": "D#",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#",
}
const pitchclassArray = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
const circleOfFifths = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
const circleOfThirds = [0, 6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 11].map(i => circleOfFifths[i])
const circleOfFFolded = [0, 3, 6, 9, 1, 4, 7, 10, 2, 5, 8, 11].map(i => circleOfFifths[i])
const circleDiffFolded = [0, 4, 1, 5, 2, 6, 3, 7, 9, 11, 8, 10].map(i => circleOfFifths[i])
// takes pitchclass 0:C; 1:Cis...
// or directly Names C, C#, D, D#, E, F, F#, G, G#, A, A#, B


// normal coloring only based on fifths, triads, fifth folded
// modes: fifths, triads, fifthsFolded
export function cyclicHarmonicColoring(value, mode = "fifths") {
    let pitch;



    // convert number → pitch name
    if (typeof value === "number") {
        pitch = pitchclassArray[value % 12];
    }
    // handle string
    else if (typeof value === "string" || value instanceof String) {
        pitch = value;

        // convert flats to sharps
        if (pitch.includes("b") && bToSharpMap[pitch]) {
            pitch = bToSharpMap[pitch];
        }
    }

    let t = 0;

    if (mode === "fifths") {

        const index = circleOfFifths.indexOf(pitch);
        t = index / 12;

    }
    else if (mode === "thirds") {

        const index = circleOfThirds.indexOf(pitch);
        t = index / 12;

    }
    else if (mode === "fifthsFolded") {

        const index = circleOfFFolded.indexOf(pitch);
        t = index / 12;
        // stretch to 4 rotations, then wrap

    }
    else if (mode === "fifthsFoldedOther") {

        const index = circleDiffFolded.indexOf(pitch);
        t = index / 12;
        // stretch to 4 rotations, then wrap

    }

    // return color
    return phaseInterpolate(t)
    //return phase12[Math.round(t * 12) % 12]
    //return d3.interpolateSinebow(t);
}
