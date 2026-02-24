<script>
    import Overview_LineUp from './Overview_LineUp.svelte';
    import Overview_PCP from './Overview_PCP.svelte';
    import Piano from "./Piano.svelte";

    export let type;
    export let visProps;

    let someValue = "overview_LineUp";

    const VIS_TYPES = {
        overview_LineUp: Overview_LineUp,
        overview_PCP: Overview_PCP,
        piano: Piano,
    };
</script>


<section class="container">
    <svelte:component this={VIS_TYPES[type]} {...visProps}/>
</section>


{#if type == someValue}
    <p>{type} is equal to {someValue}</p>
{:else}
    <p> {type} is not equal to {someValue}</p>
{/if}

<style>
    .container {
        border: solid 1px black;
        margin: auto;
    }
</style>