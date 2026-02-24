<script>
    import PianoRoll from "./PianoRoll.svelte";
    import {music, process_melody_for_visualization} from "../state.svelte.js";

    let example_melody = {
        "note_durations": [
            8,
            8,
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
            2,
            10
        ],
        "note_pitches": [
            "C1",
            "B20",
            "B4",
            "C3",
            "E4",
            "F4",
            "F#4",
            "G4",
            "D4",
            "D#4",
            "A#4",
            "G#4",
            "A4",
            "C#5",
            "C#4",
            "B4",
            "C3"
        ],
        "note_pitches_midi": [
            0,
            127,
            11,
            0,
            4,
            5,
            6,
            7,
            2,
            3,
            10,
            8,
            9,
            1,
            1,
            11,
            0
        ],
        "note_pitch_classes": [
            0,
            11,
            11,
            0,
            4,
            5,
            6,
            7,
            2,
            3,
            10,
            8,
            9,
            1,
            1,
            11,
            0
        ],
        "note_starting_times": [
            3,
            3,
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
            14,
            4
        ]
    }

    let other_example_melody = {
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
            1,
            1.5,
            0.5,
            2
        ],
        "note_pitches": [
            "B4",
            "B4",
            "E4",
            "E4",
            "B4",
            "G5",
            "D4",
            "A4",
            "E4",
            "E4",
            "A4",
            "B5",
            "B4",
            "C5",
            "B4"
        ],
        "note_pitches_midi": [
            11,
            11,
            2,
            2,
            11,
            4,
            10,
            6,
            2,
            2,
            6,
            22,
            11,
            23,
            11
        ],
        "note_pitch_classes": [
            11,
            11,
            4,
            4,
            11,
            7,
            2,
            9,
            4,
            4,
            9,
            11,
            11,
            0,
            11
        ],
        "note_starting_times": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13.5,
            14
        ]
    }

    let alle_meine_entchen = {
        "note_durations": [
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            4.0,
            1.0,
            1.0,
            1.0,
            1.0,
            4.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            4.0
        ],
        "note_pitch_classes": [
            0,
            2,
            4,
            5,
            7,
            7,
            9,
            9,
            9,
            9,
            7,
            9,
            9,
            9,
            9,
            7,
            5,
            5,
            5,
            5,
            4,
            4,
            7,
            7,
            7,
            7,
            0
        ],
        "note_pitches": [
            "C4",
            "D4",
            "E4",
            "F4",
            "G4",
            "G4",
            "A4",
            "A4",
            "A4",
            "A4",
            "G4",
            "A4",
            "A4",
            "A4",
            "A4",
            "G4",
            "F4",
            "F4",
            "F4",
            "F4",
            "E4",
            "E4",
            "G4",
            "G4",
            "G4",
            "G4",
            "C4"
        ],
        "note_pitches_midi": [
            60,
            62,
            64,
            65,
            67,
            67,
            69,
            69,
            69,
            69,
            67,
            69,
            69,
            69,
            69,
            67,
            65,
            65,
            65,
            65,
            64,
            64,
            67,
            67,
            67,
            67,
            60
        ],
        "note_starting_times": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            6.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            30.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0
        ]
    }

    let own_melody = {
        "note_durations": [
            1.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            1.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            1.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            1.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            4.0
        ],
        "note_pitch_classes": [
            6,
            8,
            9,
            6,
            2,
            6,
            1,
            8,
            9,
            6,
            2,
            6,
            11,
            8,
            6,
            2,
            11,
            2,
            9,
            8,
            9,
            8,
            6,
            5,
            6
        ],
        "note_pitches": [
            "F#4",
            "G#4",
            "A4",
            "F#4",
            "D4",
            "F#4",
            "C#4",
            "G#4",
            "A4",
            "F#4",
            "D4",
            "F#4",
            "B3",
            "G#4",
            "F#4",
            "D4",
            "B3",
            "D4",
            "A4",
            "G#4",
            "A4",
            "G#4",
            "F#4",
            "E#4",
            "F#4"
        ],
        "note_pitches_midi": [
            66,
            68,
            69,
            66,
            62,
            66,
            61,
            68,
            69,
            66,
            62,
            66,
            59,
            68,
            66,
            62,
            59,
            62,
            69,
            68,
            69,
            68,
            66,
            65,
            66
        ],
        "note_starting_times": [
            0.0,
            1.5,
            2.0,
            2.5,
            3.0,
            3.5,
            4.0,
            5.5,
            6.0,
            6.5,
            7.0,
            7.5,
            8.0,
            9.5,
            10.0,
            10.5,
            11.0,
            11.5,
            12.0,
            13.5,
            14.0,
            14.5,
            15.0,
            15.5,
            16.0
        ]
    }


    function getExampleMelody() {
        //music.melody = example_melody;
        music.melody = alle_meine_entchen;
        music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
    }

    function getOtherExampleMelody() {
        //music.melody = other_example_melody;
        music.melody = own_melody;
        music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
    }

    async function getMelody() {
        //FIXME error handling when server response is in some way failing + communication to user
        const response = await fetch('http://127.0.0.1:5000/melody');
        music.melody = await response.json();
        music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
    }
</script>


<button id="btn-getMelody" class="button_class" onclick={getMelody}>
    Get melody
</button>
<button id="btn-getExampleMelody" class="button_class" onclick={getExampleMelody}>
    Get example melody
</button>
<button id="btn-getOtherExampleMelody" class="button_class" onclick={getOtherExampleMelody}>
    Get other example melody
</button>


<!--viewbox: "0 -23 16 24",-->
<!--viewbox: "0 -135 16 140",-->
<PianoRoll
        data={{
            music_notes: music.melody,
            coloring: "pitch_class",
            viewbox: "default",
            width: '100%',
            height: '100%'
        }}
/>

<style>
    button {
        background-color: #fff;
    }
</style>