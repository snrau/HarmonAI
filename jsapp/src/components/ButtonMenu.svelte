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
        getUploadedMelody,
    } from "../helper/servercomms.js";
    import { harmonizations_for_own_melody } from "../helper/examples.js";

    function getExampleHarmonizations() {
        //music.harmonizations = alle_meine_entchen_harmonizations;
        music.harmonizations = harmonizations_for_own_melody;
        getMetrics();
    }
    let fileInput;
    let selectedFileName = "";
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
<input
    class="hidden-input"
    type="file"
    accept=".mxl,.xml,.musicxml,.mid,.midi"
    onchange={getUploadedMelody}
    bind:this={fileInput}
/>
<button onclick={() => fileInput.click()}> Upload file </button>
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
    Get Existing Har
</button>

<button
    id="btn-getExampleHarmonizations"
    class="button_class"
    onclick={getExampleHarmonizations}
>
    Get Example Har2
</button>

<button
    id="btn-saveSelectedHarmonizations"
    class="button_class"
    onclick={saveSelectedHarmonizations}
>
    Save selected harmonization(s)
</button>

<style>
    #btn-getMelody,
    #btn-getExampleHarmonizations,
    #btn-getExampleMelody {
        background-color: #ffffff;
    }

    button {
        background-color: #5f5f5f;
    }
    .hidden-input {
        display: none;
    }
</style>
