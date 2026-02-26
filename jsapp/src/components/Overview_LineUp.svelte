<script>
    //import * as LineUpJS from "lineupjs";
    let container;

    // generate some data
    const arr = [];
    const cats = ['c1', 'c2', 'c3'];
    for (let i = 0; i < 100; ++i) {
        arr.push({
            a: Math.random() * 10,
            d: 'Row ' + i,
            cat: cats[Math.floor(Math.random() * 3)],
            cat2: cats[Math.floor(Math.random() * 3)]
        })
    }

    //const lineup_1 = window.LineUpJS.asLineUp(document.body, arr);


    function showLineUp() {
        const arr = [];
        const cats = ['c1', 'c2', 'c3'];
        const numbers = [3, 2, 3, 4];
        for (let i = 0; i < 100; ++i) {
            let numbers_array = [Math.random() * 3, Math.random() * 5, Math.random() * 10, Math.random() * 8, Math.random() * 10];
            let avg_numbers = 0;
            for (let j = 0; j < numbers_array.length; ++j) {
                avg_numbers += numbers_array[j];
            }
            avg_numbers = avg_numbers / numbers_array.length;

            arr.push({
                a: Math.random() * 10,
                d: 'Row ' + i,
                cat: cats[Math.floor(Math.random() * 3)],
                cat2: cats[Math.floor(Math.random() * 3)],
                numeric_evolution: numbers_array,
                avg: avg_numbers
            })
        }
//const lineup_basic = window.LineUpJS.asLineUp(document.body, arr);
        const builder = window.LineUpJS.builder(arr);

// manually define columns
        builder
            .column(window.LineUpJS.buildStringColumn('d').label('Label').width(100))
            .column(window.LineUpJS.buildCategoricalColumn('cat', cats).color('green'))
            .column(window.LineUpJS.buildCategoricalColumn('cat2', cats).color('blue'))
            //.column(LineUpJS.buildCategoricalColumn('numeric_evolution', numbers).color('red'))
            .column(window.LineUpJS.buildNumberColumn('numeric_evolution', [0, 10]).asArray(["a", "b", "c", "d", "e"]).color('red'))
            .column(window.LineUpJS.buildNumberColumn('a', [0, 10]).color('blue'))
            .column(window.LineUpJS.buildNumberColumn('avg', [0, 10]).color('darkred'));

// and two rankings
        const ranking = window.LineUpJS.buildRanking()
            .supportTypes()
            .allColumns() // add all columns
            .impose('a+cat2', 'a', 'cat2')  // create composite column
            //.groupBy('cat')
            //.sortBy('a', 'desc');

        builder
            .defaultRanking()
            .ranking(ranking);

        //const lineup = builder.buildTaggle(document.body);

        //change of innerHTML needs to come before adding lineup for some reason
        //document.getElementById("lineup").innerHTML = "";
        const lineup = builder.build(container);
    }

    function test(){
        // generate some data
        const arr = [];
        const cats = ['c1', 'c2', 'c3'];
        for (let i = 0; i < 100; ++i) {
            arr.push({
                a: Math.random() * 10,
                d: 'Row ' + i,
                cat: cats[Math.floor(Math.random() * 3)],
                cat2: cats[Math.floor(Math.random() * 3)],
            });
        }
        // arr from before
        const builder = window.LineUpJS.builder(arr);

// manually define columns
        builder
            .column(window.LineUpJS.buildStringColumn('d').label('Label').width(100))
            .column(window.LineUpJS.buildCategoricalColumn('cat', cats).color('green'))
            .column(window.LineUpJS.buildCategoricalColumn('cat2', cats).color('blue'))
            .column(window.LineUpJS.buildNumberColumn('a', [0, 10]).color('blue'));

// and two rankings
        const ranking = window.LineUpJS.buildRanking()
            .supportTypes()
            .allColumns() // add all columns
            .impose('a+cat', 'a', 'cat2'); // create composite column
    //.groupBy('cat')
            //.sortBy('a', 'desc')


        builder
            .defaultRanking()
            .ranking(ranking);

        const lineup = builder.build(container);
    }
</script>


<h2>Demo JavaScript in Body</h2>

<div id="lineup" bind:this={container} style="width:1600px;height:1000px;">Here should appear lineup.</div>

<button type="button" onclick={test}>Show LineUp</button>


<style>

    body {
        margin: 0;
        padding: 0;
    }

    .lu {
        clear: both;
        position: absolute;
        top: 1px;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 0;
    }
</style>

