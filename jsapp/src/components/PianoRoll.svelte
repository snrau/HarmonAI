<script>
    import {
        get_color_for_metric,
        getPitchClassColor,
    } from "../helper/coloring.js";
    import {
        music,
        process_harmonizations_for_visualization,
        selectedIndex,
        smallest_duration_considered,
    } from "../state.svelte.js";
    let properties = $props();
    let notes = $derived(properties.data.music_notes);
    let width = $derived(properties.data.width);
    let height = $derived(properties.data.height);
    let number_of_smallest_units_in_piece = $derived.by(() => {
        return Math.round(
            (music.meta["latest_end"] - music.meta["earliest_start"]) /
                smallest_duration_considered,
        );
    });
    let viewbox_attributes = $derived.by(() => {
        if (properties.data.viewbox !== "default") {
            // TODO check correct input format
            return String(properties.data.viewbox);
        } else {
            // get minimal all showing Viewbox
            if (number_of_notes <= 0) {
                return "0 0 20 10";
            } else {
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
        let colors = [];
        if ($selectedIndex !== -1) {
            const colorPalet = get_color_for_metric(
                "CT_class_prog",
                process_harmonizations_for_visualization([
                    properties.data.harmonization,
                ])[0],
                number_of_notes,
            );
            for (let i = 0; i < number_of_notes; ++i) {
                colors.push(colorPalet[i]);
            }
            return colors;
        } else {
            for (let i = 0; i < number_of_notes; ++i) {
                colors.push("#666");
            }
        }

        return colors;
    });

    let number_of_notes = $derived.by(() => {
        if (Object.keys(notes).length === 0) {
            return 0;
        } else {
            return notes["note_pitches"].length;
        }
    });
</script>

<div>
    {#if number_of_notes > 0}
        <!--
        <p>min_x: {Math.min(...notes["note_starting_times"])}</p>
        <p>min_y: {-1 * Math.max(...notes["note_pitches_midi"])}</p>
        <p>max_y: {-1 * Math.min(...notes["note_pitches_midi"])}</p>
        <p>
            min_height: {Math.abs(-1 * Math.max(...notes["note_pitches_midi"]) - -1 * Math.min(...notes["note_pitches_midi"])) + 1}</p>
        -->
        <svg
            {width}
            {height}
            viewBox={viewbox_attributes}
            style="border:1px solid black"
            preserveAspectRatio="none"
        >
            <!--        for each midi pitch draw a background line that is colorable  (Midi values are constrained to the space 0-127)-->
            <!-- somehow determine color by a function that can use different strategies for coloring (e.g. alternating two colors, pitchclass, consonance, ...) -->
            {#each Array(128) as _, i}
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

            {#each Array(number_of_notes) as _, i}
                <rect
                    x={notes["note_starting_times"][i]}
                    y={-1 * notes["note_pitches_midi"][i]}
                    width={notes["note_durations"][i]}
                    height={1}
                    fill={coloring[i]}
                    rx={0.2}
                />
            {/each}
        </svg>
    {/if}
</div>

<!--
<p>Number of notes: {number_of_notes}</p>
-->

<style>
    div {
        width: 100%;
        height: 100%;
    }
    /* The circles will transition to their new state using css. */
    circle {
        transition: all 0.5s ease;
    }

    rect {
        transition: all 0.5s ease;
    }
</style>
