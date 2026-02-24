<script>
    import TestPrintData from './TestPrintData.svelte';
    let cached_melody = {
        "note_durations": [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1.5,
            0.5,
            2
        ],
        "note_pitches": [
            "B4",
            "B4",
            "E5",
            "E5",
            "B4",
            "E5",
            "D5",
            "E5",
            "B4",
            "G#4",
            "A4",
            "B4",
            "C#5",
            "B4"
        ],
        "note_starting_times": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            8,
            9,
            10,
            11,
            12,
            13.5,
            14
        ]
    }
    let cached_harmonizations = [{
        "AI_Model": "AutoHarmonizer",
        "chord_durations": [
            4,
            4,
            2,
            6
        ],
        "chord_starting_times": [
            0,
            4,
            8,
            10
        ],
        "chord_symbols": [
            "E",
            "E",
            "A",
            "E"
        ],
        "note_durations": [
            4,
            4,
            4,
            4,
            4,
            4,
            2,
            2,
            2,
            6,
            6,
            6
        ],
        "note_pitches": [
            "E3",
            "G#3",
            "B3",
            "E3",
            "G#3",
            "B3",
            "A2",
            "C#3",
            "E3",
            "E3",
            "G#3",
            "B3"
        ],
        "note_starting_times": [
            0,
            0,
            0,
            4,
            4,
            4,
            8,
            8,
            8,
            10,
            10,
            10
        ],
        "rythm_density": "0.8"
    },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "E-",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "Eb3",
                "G3",
                "Bb3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.81"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.82"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.83"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.84"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.85"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.86"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.87"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "E"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G#3",
                "B3"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.88"
        },
        {
            "AI_Model": "AutoHarmonizer",
            "chord_durations": [
                4,
                4,
                2,
                6
            ],
            "chord_starting_times": [
                0,
                4,
                8,
                10
            ],
            "chord_symbols": [
                "Em",
                "E",
                "A",
                "Em"
            ],
            "note_durations": [
                4,
                4,
                4,
                4,
                4,
                4,
                2,
                2,
                2,
                6,
                6,
                6
            ],
            "note_pitches": [
                "E3",
                "G3",
                "B3",
                "E3",
                "G#3",
                "B3",
                "A2",
                "C#3",
                "E3",
                "E3",
                "G3",
                "B1"
            ],
            "note_starting_times": [
                0,
                0,
                0,
                4,
                4,
                4,
                8,
                8,
                8,
                10,
                10,
                10
            ],
            "rythm_density": "0.89"
        }
    ];
    let props = $props();
    let testData = $state([{"test": -1, "data": -2}, {"test": 3, "data": 4}]);


    function getHarmonizations() {
        //TODO implement
        //changeData(props.data);
        //generateDummyData(props.data);
        //getTestData('http://127.0.0.1:5555/static_test_Data_from_file');
        testData = {
            "harmonizations": cached_harmonizations,
            "melody": cached_melody
        };
    }

    async function getMetrics() {
        const response = await fetch('http://127.0.0.1:5000/metrics', {
            method: 'POST',
            body: JSON.stringify(testData),
            headers: {
                "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
                "Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
                "Content-Type": "application/json", // this shows the expected content type
                "Access-Control-Allow-Origin": "*"
            }
        });
        testData = await response.json();
    }

    async function getHarmonizationsAutoharmonizer() {
        //TODO the computations take their time... add info for the user that it is working in the background and to be patient?
        //fetch harmonizations from AutoHarmonizer
        const AI_response = await fetch('http://127.0.0.1:5555/autoharmonizer');
        testData = await AI_response.json();
        // probably due to "await" the request for metrics calculation starts only when the above is received

        // TODO here would be the request for variants within chords of a harmonization

        await getMetrics();
    }


    function changeData(data) {
        data[0] = ["test", [1, Math.random(), 3], 0];
    }

    function generateDummyData(array) {
        // generate some data
        const cats = ['c1', 'c2', 'c3'];
        for (let i = 0; i < 5; ++i) {
            array.push(
                ["label_test", [9, 9, 9], Math.floor(Math.random() * 20)],
                ["label_test", [9, 9, 9], 50000]
            );
        }
    }


    function getTestData(url) {
        fetch(url)
            .then(d => d.text())
            .then(d => (testData = d));
    }
</script>


<button onclick={getHarmonizationsAutoharmonizer}>
    Generate Harmonizations with AutoHarmonizer
</button>

<button onclick={getHarmonizations}>
    Generate Harmonizations
</button>

<button onclick={getMetrics}>
    test metrics retrieval
</button>

<p>testData: {testData}</p>
<TestPrintData data={testData}/>
<p>End generate harmonizations </p>