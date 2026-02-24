<script>
    let music = $props();
    let notes = $derived(music.data.music_notes);
    let width = $derived(music.data.width);
    let height = $derived(music.data.height);
    let viewbox_attributes = $derived.by(() => {
        if (music.data.viewbox !== "default") {
            // TODO check correct input format
            return String(music.data.viewbox);
        } else {
            // get minimal all showing Viewbox
            if (number_of_notes <= 0) {
                return "0 0 20 10";
            } else {
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

    let coloring = $derived.by(() => {
        let colors = [];
        if (music.data.coloring === "pitch_class") {
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


    let number_of_notes = $derived.by(() => {
        if (Object.keys(notes).length === 0) {
            return 0;
        } else {
            return notes["note_pitches"].length;
        }
    });


</script>


<div>
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
        <svg width={width}
             height={height}
             viewBox={viewbox_attributes}
             style="border:1px solid black"
             preserveAspectRatio="none">

            <!--        for each midi pitch draw a background line that is colorable  (Midi values are constrained to the space 0-127)-->
            <!-- somehow determine color by a function that can use different strategies for coloring (e.g. alternating two colors, pitchclass, consonance, ...) -->
            {#each Array(128) as _, i}
                <line
                        x1={viewbox_attributes.split(" ")[0]}
                        y1={-1 * i + 0.5}
                        x2={viewbox_attributes.split(" ")[0] + viewbox_attributes.split(" ")[2]}
                        y2={-1 * i + 0.5}
                        style="stroke-width:0.8;opacity:15%"
                        stroke={getPitchClassColor(i % 12, "black_and_white")}
                />
            {/each}

            {#each Array(number_of_notes) as _, i}
                <rect x={notes["note_starting_times"][i]}
                      y={-1 * notes["note_pitches_midi"][i]}
                      width={notes["note_durations"][i]}
                      height={1}
                      fill={coloring[i]}
                      rx={0.2}/>
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