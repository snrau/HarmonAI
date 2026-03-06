<script>
    import {
        get_color_for_metric,
        get_typicality_of_chords_Color,
        getPitchClassColor,
    } from "../helper/coloring.js";
    import {
        music,
        process_harmonizations_for_visualization,
        smallest_duration_considered,
    } from "../state.svelte.js";
    import * as d3 from "d3";

    let properties = $props();
    let notes_harmonization = $derived(
        process_harmonizations_for_visualization([
            properties.data.music_notes,
        ])[0],
    );
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
                    note_ending_times.push(
                        notes["note_starting_times"][i] +
                            notes["note_durations"][i],
                    );
                }
                let min_width = Math.max(...note_ending_times);

                let max_y = -1 * Math.min(...notes["note_pitches_midi"]);
                let min_height = Math.abs(min_y - max_y) + 1;

                return min_x + " " + min_y + " " + min_width + " " + min_height;
            }
        }
    });

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

        // default is all notes are black
        for (let i = 0; i < number_of_notes; ++i) {
            colors.push("black");
        }
        return colors;
    });

    let coloring_note_center = $derived.by(() => {
        return get_color_for_metric(
            properties.data.coloring_note_center,
            notes_harmonization,
            number_of_smallest_units_in_piece,
        );
    });

    let coloring_background = $derived.by(() => {
        return get_color_for_metric(
            properties.data.coloring_background,
            notes_harmonization,
            number_of_smallest_units_in_piece,
        );
    });

    let coloring_chord_bar = $derived.by(() => {
        return get_color_for_metric(
            properties.data.coloring_chord_bar,
            notes_harmonization,
            number_of_smallest_units_in_piece,
        );
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
        return Math.round(
            (music.meta["latest_end"] - music.meta["earliest_start"]) /
                smallest_duration_considered,
        );
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

            <br />
        {/if}
        <svg
            {width}
            height={0.72 * height}
            viewBox={viewbox_attributes}
            style="border:1px solid black;background-color: white"
            preserveAspectRatio="none"
        >
            <!-- background vertical units 
            {#each Array(number_of_smallest_units_in_piece) as _, i}
                <rect
                    x={i * smallest_duration_considered}
                    y={viewbox_attributes.split(" ")[1]}
                    width={smallest_duration_considered}
                    height={viewbox_attributes.split(" ")[3]}
                    fill={coloring_background[i]}
                    opacity="60%"
                />
            {/each}
            -->

            <!-- background horizontal lines -->
            <!--        for each midi pitch draw a background line that is colorable  (Midi values are constrained to the space 0-127)-->
            <!-- somehow determine color by a function that can use different strategies for coloring (e.g. alternating two colors, pitchclass, consonance, ...) -->
            {#each Array(128) as _, i}
                <!-- non-opaque 
                <line
                    x1={viewbox_attributes.split(" ")[0]}
                    y1={-1 * i + 0.5}
                    x2={viewbox_attributes.split(" ")[0] +
                        viewbox_attributes.split(" ")[2]}
                    y2={-1 * i + 0.5}
                    style="stroke-width:0.4;opacity:50%"
                    stroke="#a0a0a0"
                />
                -->
                <!-- colorable -->
                <line
                    x1={viewbox_attributes.split(" ")[0]}
                    y1={-1 * i + 0.5}
                    x2={viewbox_attributes.split(" ")[0] +
                        viewbox_attributes.split(" ")[2]}
                    y2={-1 * i + 0.5}
                    style="stroke-width:0.9;opacity:15%"
                    stroke={getPitchClassColor(i % 12, "black_and_white")}
                />
            {/each}

            <!-- harmonization notes -->
            {#each Array(number_of_notes) as _, i}
                <rect
                    x={notes_harmonization["note_starting_times"][i]}
                    y={-1 * notes_harmonization["note_pitches_midi"][i]}
                    width={notes_harmonization["note_durations"][i]}
                    height={1}
                    fill={"#666"}
                    //stroke={coloring[i]}
                    stroke-width={0.15}
                    stroke-opacity="1"
                    rx={0.2}
                />
            {/each}
        </svg>

        <!-- make the bands with roman numerals and chord symbols  (below the pianoroll if pianoroll displays a harmonization) -->
        <svg
            {width}
            height={0.1 * height}
            style="border:1px solid black"
            viewBox={viewbox_attributes.split(" ")[0] +
                " 0 " +
                viewbox_attributes.split(" ")[2] +
                " 2"}
            preserveAspectRatio="none"
        >
            <!-- metric encoding rectangles -->
            {#each Array(number_of_smallest_units_in_piece) as _, i}
                <rect
                    x={i * smallest_duration_considered}
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
                <text
                    x={notes_harmonization["chord_starting_times"][i]}
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
        <!-- roman numerals -->
        <svg
            {width}
            height={0.1 * height}
            style="border:1px solid black"
            viewBox={viewbox_attributes.split(" ")[0] +
                " 0 " +
                viewbox_attributes.split(" ")[2] +
                " 2"}
            preserveAspectRatio="none"
        >
            {#each Array(number_of_chords) as _, i}
                <!-- rectangles for colored background -->
                <rect
                    x={notes_harmonization["chord_starting_times"][i]}
                    y="0"
                    width={notes_harmonization["chord_durations"][i]}
                    height={2}
                    fill={get_typicality_of_chords_Color(
                        notes_harmonization[
                            "typical_chord_progression_coverage_per_chord"
                        ][i],
                    )}
                >
                    {notes_harmonization["chord_symbols"][i]}
                </rect>
                <!-- actual roman numerals -->
                <text
                    x={notes_harmonization["chord_starting_times"][i]}
                    y="1.3"
                    font-size="1"
                    fill="white"
                >
                    {notes_harmonization["roman_numerals"][i]}
                </text>
            {/each}
        </svg>
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
