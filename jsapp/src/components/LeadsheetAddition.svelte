<script>
    import { music } from "../state.svelte.js";
    import Advanced_PianoRoll from "./Advanced_PianoRoll.svelte";
    import PianoRollAddition from "./PianoRollAddition.svelte";

    let properties = $props();
    let notes = $derived(properties.data.music_notes);
    let width = $derived(properties.data.width);
    let heightpercent = $derived(properties.data.height);
    const height = window.innerHeight * (parseFloat(heightpercent) / 100) - 1;
    let coloring_melody = $derived(properties.data.coloring_melody);
    let coloring_harmonization = $derived(
        properties.data.coloring_harmonization,
    );
</script>

<div id="harmonic_leadsheet_div">
    <!-- Melody -->
    <PianoRollAddition
        data={{
            music_notes: notes,
            coloring: coloring_harmonization,
            coloring_background: "CTD",
            coloring_note_center: "CT_class",
            coloring_chord_bar: "PCS",
            viewbox: music.meta.viewbox_harmonizations,
            width: width,
            height: height,
        }}
    />
</div>

<style>
    div {
        background-color: black;
        border: 2px solid black;
        overflow: hidden;
    }
</style>
