<script>
    import Demo_stuff from './Demo_stuff.svelte';
    import Nested from './components/Nested.svelte';
    import VisContainer from './components/VisContainer.svelte';
    import TestPrintData from './components/TestPrintData.svelte';
    import Melody from './components/Melody.svelte';
    import GenerateHarmonizations from './components/GenerateHarmonizations.svelte';

    let data = $state([["label_1", [1, 1, 3], 0], ["label_2", [1, 2, 3], 5], ["label_3", [1, 2, 3], 0]]);


    let rand = $state(-1);

    function getRand() {
        fetch('http://127.0.0.1:5000/rand')
            .then(d => d.text())
            .then(d => (rand = d));
    }
</script>

<main>

    <text>Your number is {rand}!</text>
    <button onclick={getRand}>Get a random number</button>


    <Melody/>
    <GenerateHarmonizations data={data}/>
    <TestPrintData data={data}/>

    <Nested/>

    <VisContainer type={"piano"} visProps={{}}/>
    <VisContainer type={"overview_PCP"} visProps={{}}/>
    <VisContainer type={"overview_LineUp"} visProps={{}}/>


    <Demo_stuff/>
</main>

