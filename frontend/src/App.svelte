<script>
    import LineUp from "./new_Components/LineUp.svelte";
    import GenerateHarmonizations from "./new_Components/GenerateHarmonizations.svelte";
    import Melody from "./new_Components/Melody.svelte";
    import PianoRoll from "./new_Components/PianoRoll.svelte";
    import {music} from "./state.svelte.js";
    import Save_and_Load from "./new_Components/Save_and_Load.svelte";
    import Harmonic_Leadsheet from "./new_Components/Harmonic_Leadsheet.svelte";

    //     viewbox: "0 -60 16 20"

    window.onload = repositionButtons
    window.onresize = repositionButtons

    function repositionButtons() {
        let controller = document.getElementById("buttons-container");
        controller.appendChild(document.getElementById("btn-getMelody"));
        controller.appendChild(document.getElementById("btn-getExampleMelody"));
        controller.appendChild(document.getElementById("btn-getOtherExampleMelody"));

        controller.appendChild(document.getElementById("btn-generateHarmonizationsWithAutoHarmonizer"));
        controller.appendChild(document.getElementById("btn-getExistingHarmonizations"));
        controller.appendChild(document.getElementById("btn-getExampleHarmonizations"));
        controller.appendChild(document.getElementById("btn-cacheCurrentHarmonizations"));
        controller.appendChild(document.getElementById("btn-getHarmonizationsFromCache"));

        controller.appendChild(document.getElementById("btn-saveSelectedHarmonizations"));
    }
</script>

<main>
    <div id="page-layout-container">
        <div id="melody-container">
            <Melody/>
        </div>
        <div id="buttons-container"></div>
        <div id="lineup-container">
            <LineUp/>
        </div>

        <div id="selected-harmonizations-container">
            {#each music.selected_harmonizations as harmonization}
                <Harmonic_Leadsheet data={{
                    music_notes: harmonization,
                    coloring_melody: "pitch_class",
                    coloring_harmonization: "pitch_class",
                    width: '100%',
                    height: 240,
                }}/>
                <div class="horizontal-divider-div"></div>
            {/each}
        </div>
    </div>

    <GenerateHarmonizations/>
    <Save_and_Load/>

    <div class="highlighted-harmonization-container">
        {#if music.highlighted_harmonization_index !== -1}
        <Harmonic_Leadsheet data={{
                        music_notes: music.highlighted_harmonization,
                        coloring_melody: "pitch_class",
                        coloring_harmonization: "pitch_class",
                        width: '100%',
                        height: 200,
                    }}/>
        {/if}
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
        grid-template-columns: 1fr 440px;
        grid-template-rows: 18% 35% auto;
        grid-gap: 3px;
    }

    #melody-container {
        border: black solid 2px;
        grid-column-start: 1;
        grid-column-end: 2;

    }

    #buttons-container {
        border: black solid 2px;
        grid-column-start: 2;
        grid-column-end: 3;
        display: grid;
        grid-auto-columns: auto auto;
        overflow: auto;
    }

    #lineup-container {
        border: black solid 2px;
        grid-column-start: 1;
        grid-column-end: 3;
    }

    #selected-harmonizations-container {
        border: black solid 2px;
        grid-column-start: 1;
        grid-column-end: 3;
        overflow-y: auto;
    }

    .horizontal-divider-div {
        width: 100%;
        height: 5px;
        color: white;
    }

    .highlighted-harmonization-container {
        position: fixed;
        width: 99%;
        top: 1px;
        left: 50%;
        transform: translateX(-50%);
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
