<script>
    import LineUp from "./components/LineUp.svelte";
    import ButtonMenu from "./components/ButtonMenu.svelte";
    import { music } from "./state.svelte.js";
    import Harmonic_Leadsheet from "./components/Harmonic_Leadsheet.svelte";
    import PianoRoll from "./components/PianoRoll.svelte";
    import LeadsheetAddition from "./components/LeadsheetAddition.svelte";
    import CircleOfFifths from "./components/CircleOfFifths.svelte";

    //     viewbox: "0 -60 16 20"

    /*
    window.onload = repositionButtons;
    window.onresize = repositionButtons;

    function repositionButtons() {
        let controller = document.getElementById("buttons-container");
        controller.appendChild(document.getElementById("btn-getMelody"));
        controller.appendChild(document.getElementById("btn-getExampleMelody"));
        controller.appendChild(
            document.getElementById("btn-getOtherExampleMelody"),
        );

        controller.appendChild(
            document.getElementById(
                "btn-generateHarmonizationsWithAutoHarmonizer",
            ),
        );
        controller.appendChild(
            document.getElementById("btn-getExistingHarmonizations"),
        );
        controller.appendChild(
            document.getElementById("btn-getExampleHarmonizations"),
        );

        controller.appendChild(
            document.getElementById("btn-saveSelectedHarmonizations"),
        );
    }
    */
</script>

<main>
    <div id="page-layout-container">
        <div id="melody-container">
            <PianoRoll
                data={{
                    music_notes: music.melody,
                    harmonization: music.selected_harmonizations[0],
                    coloring: "pitch_class",
                    viewbox: "default",
                    width: "100%",
                    height: "100%",
                }}
            />
        </div>
        <div id="circle-of-fifths-container">
            <CircleOfFifths />
        </div>

        <div id="buttons-container">
            <ButtonMenu />
        </div>

        <div id="selected-harmonizations-container">
            {#each music.selected_harmonizations as harmonization}
                <LeadsheetAddition
                    data={{
                        music_notes: harmonization,
                        coloring_melody: "pitch_class",
                        coloring_harmonization: "pitch_class",
                        width: "100%",
                        height: "29%",
                    }}
                />
                <div class="horizontal-divider-div"></div>
            {/each}
        </div>
        <div class="highlighted-harmonization-container">
            {#if music.highlighted_harmonization_index !== -1}
                <Harmonic_Leadsheet
                    data={{
                        music_notes: music.highlighted_harmonization,
                        coloring_melody: "pitch_class",
                        coloring_harmonization: "pitch_class",
                        width: "100%",
                        height: "29%",
                    }}
                />
            {/if}
        </div>
        <div id="lineup-container">
            <LineUp />
        </div>
    </div>
</main>

<style>
    #page-layout-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        height: 99%;
        width: 99%;
        display: grid;
        grid-template-columns: 1fr 440px 70px 370px;
        grid-template-rows: 18% 31% 50%;
        grid-gap: 3px;
        overflow: hidden;
    }

    #melody-container {
        border: black solid 2px;
        grid-column-start: 1;
        grid-column-end: 3;
    }

    #buttons-container {
        border: black solid 2px;
        grid-column-start: 4;
        grid-column-end: 5;
        display: grid;
        grid-template-columns: auto auto;
        overflow: auto;
    }
    #circle-of-fifths-container {
        grid-column-start: 3;
        grid-column-end: 4;
    }

    #lineup-container {
        border: black solid 2px;
        grid-column-start: 1;
        grid-column-end: 5;
    }

    #selected-harmonizations-container {
        grid-column-start: 1;
        grid-column-end: 3;
        overflow: hidden;
    }

    .horizontal-divider-div {
        width: 100%;
        height: 5px;
        color: white;
    }

    .highlighted-harmonization-container {
        grid-column-start: 3;
        grid-column-end: 5;
        overflow: hidden;
    }

    :global(button) {
        border-color: grey;
        font-size: small;
    }

    :global(#btn-getMelody) {
        grid-column-start: span 2;
        border: black solid 2px;
        font-weight: bold;
    }

    :global(#btn-getExampleMelody) {
        grid-column-start: span 1;
    }

    :global(#btn-getOtherExampleMelody) {
        grid-column-start: span 1;
    }

    :global(#btn-generateHarmonizationsWithAutoHarmonizer) {
        grid-column-start: span 2;
        border: black solid 2px;
        font-weight: bold;
    }

    :global(#btn-getExistingHarmonizations) {
        grid-column-start: span 1;
    }

    :global(#btn-getExampleHarmonizations) {
        grid-column-start: span 1;
    }

    :global(#btn-getHarmonizationsFromCache) {
        grid-column-start: span 1;
    }

    :global(#btn-cacheCurrentHarmonizations) {
        grid-column-start: span 1;
    }

    :global(#btn-saveSelectedHarmonizations) {
        grid-column-start: span 2;
        border: black solid 2px;
        font-weight: bold;
    }
</style>
