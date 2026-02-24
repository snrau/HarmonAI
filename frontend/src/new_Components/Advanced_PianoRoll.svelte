<script>
    import {music, process_harmonizations_for_visualization, smallest_duration_considered} from "../state.svelte.js";
    import * as d3 from "d3";

    let properties = $props();
    let notes_harmonization = $derived(process_harmonizations_for_visualization([properties.data.music_notes])[0]);
    let visualize_melody = $derived(properties.data.visualize_melody);
    let width = $derived(properties.data.width);
    let height = $derived(properties.data.height);
    let viewbox_attributes = $derived.by(() => {
        if (properties.data.viewbox !== "default") {
            // TODO check correct input format
            return String(properties.data.viewbox);
        } else {
            // get minimal all showing Viewbox
            if (number_of_notes <= 0) {
                return "0 0 20 10";
            } else {
                // make sure viewbox is computed for the notes that should be displayed
                let notes = {};
                if (visualize_melody) {
                    notes = music.melody;
                } else {
                    notes = notes_harmonization;
                }

                // actual computations
                let min_x = Math.min(...notes["note_starting_times"]);
                let min_y = -1 * Math.max(...notes["note_pitches_midi"]);

                let note_ending_times = [];
                for (let i = 0; i < notes["note_starting_times"].length; i++) {
                    note_ending_times.push(notes["note_starting_times"][i] + notes["note_durations"][i]);
                }
                let min_width = Math.max(...note_ending_times);

                let max_y = -1 * Math.min(...notes["note_pitches_midi"]);
                let min_height = Math.abs(min_y - max_y) + 1;


                return min_x + " " + min_y + " " + min_width + " " + min_height;
            }
        }
    });

    function getPitchClassColor(pitchclass, color_palette = "rainbow") {
        // TODO select useful coloring
        // rainbow
        // black white as piano tastatur
        // helle farben weiße tasten, dunkle farben schwarze tasten
        // circle of ... fifths/thirds/... or other ideas from literature

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
            }
        }
        return color_mapping[color_palette][pitchclass];
    }

    function get_color_for_metric(metric) {
        let colors = [];
        if (metric === "pitch_class_melody") {
            for (let i = 0; i < number_of_smallest_units_in_piece; ++i) {
                colors.push(getPitchClassColor(music.melody["note_pitches_midi_reflecting_durations"][i] % 12));
            }
        }
        if (metric === "PCS") {
            // here always work on the harmonization attributes, since there are the computed metrics saved
            for (let i = 0; i < notes_harmonization["PCS progression (pitch consonance score)"].length; ++i) {
                colors.push(getPCSColor(notes_harmonization["PCS progression (pitch consonance score)"][i]));
            }
        }
        if (metric === "MCTD") {
            // here always work on the harmonization attributes, since there are the computed metrics saved
            for (let i = 0; i < notes_harmonization["MCTD progression (melody tone chord tonal distance)"].length; ++i) {
                colors.push(get_MCTD_Color(notes_harmonization["MCTD progression (melody tone chord tonal distance)"][i]));
            }
        }
        if (metric === "CT_class") {
            // here always work on the harmonization attributes, since there are the computed metrics saved
            for (let i = 0; i < notes_harmonization["CT class progression (chord tone) (string labels)"].length; ++i) {
                colors.push(get_CT_class_Color(notes_harmonization["CT class progression (chord tone) (string labels)"][i]));
            }
        }
        if (metric === "typicality_of_chords") {
            // here always work on the harmonization attributes, since there are the computed metrics saved
            for (let i = 0; i < notes_harmonization["typicality_of_chords_per_chord"].length; ++i) {
                colors.push(get_typicality_of_chords_Color(notes_harmonization["typicality_of_chords_per_chord"][i]));
            }
        }
        if (metric === "CTD") {
            // here always work on the harmonization attributes, since there are the computed metrics saved
            for (let i = 0; i < notes_harmonization["CTD per chord (chord tonal distance)"].length; ++i) {
                colors.push(get_CTD_Color(notes_harmonization["CTD per chord (chord tonal distance)"][i]));
            }
        }
        return colors;
    }

    function getPCSColor(PCS_value) {
        return d3.scaleLinear([-1, 0, 1], ["darkred", "white", "darkblue"])(PCS_value);
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

    function get_typicality_of_chords_Color(value) {
        // TODO check grey values
        if (value === 0) {
            return "#aaa";
        } else if (value === 1) {
            return "darkcyan";
        }
    }

    function get_CTD_Color(value) {
        return d3.scaleLinear([0, 2], ["#ccc", "darkblue"]).unknown("white")(value);
    }

    let coloring = $derived.by(() => {
        // make sure coloring is computed for the notes that should be displayed
        let notes = {};
        if (visualize_melody) {
            notes = music.melody;
        } else {
            notes = notes_harmonization;
        }

        // compute colors
        let colors = [];
        if (properties.data.coloring === "pitch_class") {
            for (let i = 0; i < number_of_notes; ++i) {
                colors.push(getPitchClassColor(notes["note_pitch_classes"][i]));
            }
            return colors;
        }
        // TODO add further coloring options here

        // default is all notes are black
        for (let i = 0; i < number_of_notes; ++i) {
            colors.push("black");
        }
        return colors;
    });


    let coloring_note_center = $derived.by(() => {
        return get_color_for_metric(properties.data.coloring_note_center);
    });


    let coloring_background = $derived.by(() => {
        return get_color_for_metric(properties.data.coloring_background);
    });


    let coloring_chord_bar = $derived.by(() => {
        return get_color_for_metric(properties.data.coloring_chord_bar);
    });


    let number_of_notes = $derived.by(() => {
        if (visualize_melody) {
            if (Object.keys(music.melody).length === 0) {
                return 0;
            } else {
                return music.melody["note_pitches"].length;
            }
        } else {
            if (Object.keys(notes_harmonization).length === 0) {
                return 0;
            } else {
                return notes_harmonization["note_pitches"].length;
            }
        }
    });

    let number_of_chords = $derived.by(() => {
        if (Object.keys(notes_harmonization).length === 0) {
            return 0;
        } else {
            return notes_harmonization["chord_symbols"].length;
        }
    });

    let number_of_smallest_units_in_piece = $derived.by(() => {
        return Math.round((music.meta["latest_end"] - music.meta["earliest_start"]) / smallest_duration_considered);
    });


</script>


<div>
    <!--
    <p>number_of_smallest_units_in_piece: {number_of_smallest_units_in_piece}</p>
    <p>visualize_melody: {visualize_melody}</p>
    <p>number_of_notes: {number_of_notes}</p>
    -->
    {#if number_of_notes <= 0}
        <p>No notes to show.</p>
    {:else}
        <!--
        <p>min_x: {Math.min(...notes["note_starting_times"])}</p>
        <p>min_y: {-1 * Math.max(...notes["note_pitches_midi"])}</p>
        <p>max_y: {-1 * Math.min(...notes["note_pitches_midi"])}</p>
        <p>
            min_height: {Math.abs(-1 * Math.max(...notes["note_pitches_midi"]) - -1 * Math.min(...notes["note_pitches_midi"])) + 1}</p>
        -->
        {#if visualize_melody}
            <!-- make chords band -->
            <svg
                    width={width}
                    height={0.25 * height}
                    style="border:1.5px solid black"
                    viewBox={(viewbox_attributes.split(" ")[0] + " 0 " + viewbox_attributes.split(" ")[2] + " 2")}
                    preserveAspectRatio="none"
            >
                <!-- metric encoding rectangles -->
                {#each Array(number_of_smallest_units_in_piece) as _, i}
                    <rect x={i * smallest_duration_considered}
                          y="0"
                          width={smallest_duration_considered}
                          height={2}
                          fill={coloring_chord_bar[i]}
                    >
                        {notes_harmonization["chord_symbols"][i]}
                    </rect>
                {/each}
                {#each Array(number_of_chords) as _, i}
                    <!-- actual chord symbol text -->
                    <text x={notes_harmonization["chord_starting_times"][i]}
                          y="1.45"
                          font-size="1.2"
                          font-weight="bold"
                          fill="white"
                          stroke="black"
                          stroke-width="0.03"
                    >
                        {notes_harmonization["chord_symbols"][i]}
                    </text>
                {/each}
            </svg>
            <br>
        {/if}
        <svg width={width}
             height={0.8 * height}
             viewBox={viewbox_attributes}
             style="border:1.5px solid black;background-color: white"
             preserveAspectRatio="none"
        >

            <!-- background vertical units -->
            {#each Array(number_of_smallest_units_in_piece) as _, i}
                <rect x={i * smallest_duration_considered}
                      y={viewbox_attributes.split(" ")[1]}
                      width={smallest_duration_considered}
                      height={viewbox_attributes.split(" ")[3]}
                      fill={coloring_background[i]}
                      opacity="60%"
                />
            {/each}


            <!-- background horizontal lines -->
            <!--        for each midi pitch draw a background line that is colorable  (Midi values are constrained to the space 0-127)-->
            <!-- somehow determine color by a function that can use different strategies for coloring (e.g. alternating two colors, pitchclass, consonance, ...) -->
            {#each Array(128) as _, i}
                <!-- non-opaque -->
                <line
                        x1={viewbox_attributes.split(" ")[0]}
                        y1={-1 * i + 0.5}
                        x2={viewbox_attributes.split(" ")[0] + viewbox_attributes.split(" ")[2]}
                        y2={-1 * i + 0.5}
                        style="stroke-width:0.4;opacity:50%"
                        stroke="#a0a0a0"
                />
                <!-- colorable -->
                <line
                        x1={viewbox_attributes.split(" ")[0]}
                        y1={-1 * i + 0.5}
                        x2={viewbox_attributes.split(" ")[0] + viewbox_attributes.split(" ")[2]}
                        y2={-1 * i + 0.5}
                        style="stroke-width:0.3;opacity:20%"
                        stroke={getPitchClassColor(i % 12, "black_and_white")}
                />
            {/each}


            <!-- actual notes -->
            {#if visualize_melody}

                <!-- color encoding in the note centers -->
                {#each Array(number_of_smallest_units_in_piece) as _, i}
                    <rect x={i * smallest_duration_considered}
                          y={-1 * music.melody["note_pitches_midi_reflecting_durations"][i]}
                          width={smallest_duration_considered}
                          height={1}
                          fill={"black"}
                          opacity="100%"
                    />
                    <rect x={i * smallest_duration_considered}
                          y={-1 * music.melody["note_pitches_midi_reflecting_durations"][i]}
                          width={smallest_duration_considered}
                          height={1}
                          fill={coloring_note_center[i]}
                          opacity={1}
                    />
                {/each}
                <!-- melody notes -->
                {#each Array(number_of_notes) as _, i}
                    <rect x={music.melody["note_starting_times"][i]}
                          y={-1 * music.melody["note_pitches_midi"][i]}
                          width={music.melody["note_durations"][i]}
                          height={1}
                          fill-opacity="0%"
                          fill={coloring[i]}
                          stroke={getPitchClassColor(music.melody["note_pitch_classes"][i])}
                          stroke-opacity="100%"
                          stroke-width={0.15}
                          rx={0.2}/>
                {/each}

            {:else}
                <!-- harmonization notes -->
                {#each Array(number_of_notes) as _, i}
                    <rect x={notes_harmonization["note_starting_times"][i]}
                          y={-1 * notes_harmonization["note_pitches_midi"][i]}
                          width={notes_harmonization["note_durations"][i]}
                          height={1}
                          fill={coloring[i]}
                          fill-opacity="0.6"
                          stroke={coloring[i]}
                          stroke-width={0.15}
                          stroke-opacity="1"
                          rx={0.2}/>
                {/each}
            {/if}
        </svg>

        <!-- make the bands with roman numerals and chord symbols  (below the pianoroll if pianoroll displays a harmonization) -->
        {#if !visualize_melody}
            <br>
            <!-- roman numerals -->
            <svg
                    width={width}
                    height={0.2 * height}
                    style="border:1.5px solid black"
                    viewBox={(viewbox_attributes.split(" ")[0] + " 0 " + viewbox_attributes.split(" ")[2] + " 2")}
                    preserveAspectRatio="none"
            >
                {#each Array(number_of_chords) as _, i}
                    <!-- rectangles for colored background -->
                    <rect x={notes_harmonization["chord_starting_times"][i]}
                          y="0"
                          width={notes_harmonization["chord_durations"][i]}
                          height={2}
                          fill={get_typicality_of_chords_Color(notes_harmonization["typical_chord_progression_coverage_per_chord"][i])}
                    >
                        {notes_harmonization["chord_symbols"][i]}
                    </rect>
                    <!-- actual roman numerals -->
                    <text x={notes_harmonization["chord_starting_times"][i]}
                          y="1.3"
                          font-size="1"
                          fill="white"
                    >
                        {notes_harmonization["roman_numerals"][i]}
                    </text>
                {/each}
            </svg>
        {/if}
    {/if}
</div>

<!--
<p>Number of notes: {number_of_notes}</p>
-->

<style>
    /* The circles will transition to their new state using css. */
    circle {
        transition: all 0.5s ease;
    }

    rect {
        transition: all 0.5s ease;
    }
</style>