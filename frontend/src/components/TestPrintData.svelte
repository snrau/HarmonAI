<script>
    let test_src = './assets/Test_datensatz_LineUp.json';
    let properties = $props();


    // generate some data
    const arr = $state([]);
    const cats = ['c1', 'c2', 'c3'];
    for (let i = 0; i < 7; ++i) {
        arr.push({
            a: Math.random() * 10,
            d: 'Row ' + i,
            cat: cats[Math.floor(Math.random() * 3)],
            cat2: cats[Math.floor(Math.random() * 3)],
        });
    }


    function onpointerenter(event) {
        arr[2].a = 2;
    }
</script>

<p>Begin TestPrintData: </p>
<p>{properties.data.harmonizations} </p>

<div>
    {#each properties.data.harmonizations as sample, i}
        <div>
            <text {onpointerenter}> sample: Index {i}:, {sample.chord_symbols}, {sample.AI_Model}
                , {sample.chord_starting_times}, {sample.note_pitches}  </text>
        </div>
    {/each}
</div>

<div>
    {#each arr as sample, i}
        <p {onpointerenter}>Index: {i}, {sample[0]}, {sample.d}, {sample.cat}, {sample.cat2}  </p>
    {/each}
</div>


<div>
    {#each ["test", 1, [1, 2, 3]] as attributeValue, j}
        <text> test</text>
        <text> Index inner: {j}, {attributeValue} </text>
    {/each}
</div>


<p>End of TestPrintData</p>