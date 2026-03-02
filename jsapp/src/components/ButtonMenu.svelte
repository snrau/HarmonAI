<script>
    import { music } from "../state.svelte.js";

    import {
        getMetrics,
        getHarmonizationsAutoharmonizer,
        getExistingHarmonizations,
        saveSelectedHarmonizations,
        getMelody,
        getExampleMelody,
        getOtherExampleMelody,
    } from "../helper/servercomms.js";
    import {
        harmonizations_for_own_melody,
        alle_meine_entchen_harmonizations,
    } from "../helper/examples.js";

    function getExampleHarmonizations() {
        //music.harmonizations = alle_meine_entchen_harmonizations;
        music.harmonizations = harmonizations_for_own_melody;
        getMetrics();
    }
</script>

<button id="btn-getMelody" class="button_class" onclick={getMelody}>
    Get melody
</button>
<button
    id="btn-getExampleMelody"
    class="button_class"
    onclick={getExampleMelody}
>
    Get example melody
</button>
<button
    id="btn-getOtherExampleMelody"
    class="button_class"
    onclick={getOtherExampleMelody}
>
    Get other example melody
</button>
<button
    id="btn-generateHarmonizationsWithAutoHarmonizer"
    class="button_class"
    onclick={getHarmonizationsAutoharmonizer}
>
    Generate Harmonizations with AI
</button>

<button
    id="btn-getExistingHarmonizations"
    class="button_class"
    onclick={getExistingHarmonizations}
>
    Get Existing Harmonizations
</button>

<button
    id="btn-getExampleHarmonizations"
    class="button_class"
    onclick={getExampleHarmonizations}
>
    Get Example Harmonizations
</button>

<button
    id="btn-saveSelectedHarmonizations"
    class="button_class"
    onclick={saveSelectedHarmonizations}
>
    Save selected harmonization(s)
</button>

<div id="messages_div"></div>

<style>
    #btn-generateHarmonizationsWithAutoHarmonizer,
    #btn-getExistingHarmonizations,
    #btn-getExampleHarmonizations {
        background-color: #ddd;
    }

    button {
        background-color: #fff;
    }

    #messages_div {
        position: absolute;
        top: 0;
        left: 0;
        background-color: white;
        opacity: 0.6;
        color: black;
    }
</style>
