import { music, process_melody_for_visualization } from "../state.svelte.js";
import { alle_meine_entchen, own_melody } from "./examples.js";

export async function saveSelectedHarmonizations() {
    if (music.selected_harmonizations.length === 0) {
        alert("No harmonization selected.");
    } else {
        //FIXME error handling when server response is in some way (most often either server is not running or internal server error due to bug in my code) failing + communication to user
        const response = await fetch(
            "http://127.0.0.1:5000/save_harmonizations",
            {
                method: "POST",
                body: JSON.stringify({
                    harmonizations: music.selected_harmonizations,
                    melody: music.melody,
                }),
                headers: {
                    "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET", // this states the allowed methods
                    "Content-Type": "application/json", // this shows the expected content type
                    "Access-Control-Allow-Origin": "*",
                },
            },
        );
        // TODO inform user of successful saving
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "score.musicxml";
        a.click();

        URL.revokeObjectURL(url);
    }
}


export async function getMetrics() {
    //FIXME error handling when server response is in some way (most often either server is not running or internal server error due to bug in my code) failing + communication to user
    if (Object.keys(music.melody).length === 0) {
        alert('Without melody the metrics can not be calculated.');
    } else if (music.harmonizations.length === 0) {
        alert('Without harmonizations the metrics can not be calculated.');
    } else {
        document.getElementById("messages_div").innerHTML = "Computing harmonization metrics..."
        const response = await fetch('http://127.0.0.1:5000/metrics', {
            method: 'POST',
            body: JSON.stringify({ "harmonizations": music.harmonizations, "melody": music.melody }),
            headers: {
                "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
                "Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
                "Content-Type": "application/json", // this shows the expected content type
                "Access-Control-Allow-Origin": "*"
            }
        });
        document.getElementById("messages_div").innerHTML = "Status: " + response.status + ": " + response.statusText;
        let music_data = await response.json();
        music.harmonizations = music_data.harmonizations;
        music.meta = music_data.meta;
        document.getElementById("messages_div").innerHTML = "Received harmonization metrics." + " Status: " + response.status + ": " + response.statusText;
        //music.melody = music_data.melody; //should not be necessary since no changes to melody expected
    }
}


export async function getHarmonizationsAutoharmonizer() {
    //TODO the computations take their time... add info for the user that it is working in the background and to be patient?
    //FIXME error handling when server response is in some way (most often either server is not running or internal server error due to bug in my code) failing + communication to user
    if (Object.keys(music.melody).length === 0) {
        alert(
            "You need to input a melody before it is possible to harmonize it.",
        );
    } else {
        //alert('Harmonizing...'); // blocks processing
        document.getElementById("messages_div").innerHTML =
            "Generating harmonizations...";
        //fetch harmonizations from AutoHarmonizer
        const AI_response = await fetch(
            "http://127.0.0.1:5555/autoharmonizer",
            {
                method: "POST",
                body: JSON.stringify({
                    melody: music.melody,
                    rhythm_density_lower_bound: 0.7, // TODO let user pick these values
                    rhythm_density_upper_bound: 1,
                }),
                headers: {
                    "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET", // this states the allowed methods
                    "Content-Type": "application/json", // this shows the expected content type
                    "Access-Control-Allow-Origin": "*",
                },
            },
        );
        let music_data = await AI_response.json();
        //harmonizations["harmonizations"] = music_data;
        music.harmonizations = music_data;
        document.getElementById("messages_div").innerHTML =
            "Received harmonizations.";
        // probably due to "await" the request for metrics calculation starts only when the above is received

        // request for variants within chords of a harmonization
        // await getVariationsWithinChords(); // not in use, since leads to many samples but the metrics do not show differences

        //alert('Computing metrics...'); // blocks processing
        await getMetrics();

        // TODO here directly cache the data in music to somewhere?
        // currently user uses the button to have pure manual control
        //localStorage.setItem("harmonizations", JSON.stringify(music.harmonizations));
    }
}

export async function getExistingHarmonizations() {
    //TODO the computations take their time... add info for the user that it is working in the background and to be patient?
    //FIXME error handling when server response is in some way (most often either server is not running or internal server error due to bug in my code) failing + communication to user
    if (Object.keys(music.melody).length === 0) {
        alert(
            "You need to input a melody before it is possible to harmonize it.",
        );
    } else {
        //alert('Harmonizing...'); // blocks processing
        document.getElementById("messages_div").innerHTML =
            "Getting harmonizations...";
        //fetch existing harmonizations
        const AI_response = await fetch(
            "http://127.0.0.1:5555/existing_harmonizations",
        );
        music.harmonizations = await AI_response.json();
        document.getElementById("messages_div").innerHTML =
            "Received harmonizations.";
        // probably due to "await" the request for metrics calculation starts only when the above is received

        // request for variants within chords of a harmonization
        // await getVariationsWithinChords(); // not in use, since leads to many samples but the metrics do not show differences

        //alert('Computing metrics...'); // blocks processing
        await getMetrics();

        // TODO here directly cache the data in music to somewhere?
        // currently user uses the button to have pure manual control
        //localStorage.setItem("harmonizations", JSON.stringify(music.harmonizations));
    }
}


// Melodies stuff

export function getExampleMelody() {
    //music.melody = example_melody;
    music.melody = alle_meine_entchen;
    music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
}

export function getOtherExampleMelody() {
    //music.melody = other_example_melody;
    music.melody = own_melody;
    music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
}

export async function getMelody() {
    //FIXME error handling when server response is in some way failing + communication to user
    const response = await fetch('http://127.0.0.1:5000/melody');
    music.melody = await response.json();
    music.melody["note_pitches_midi_reflecting_durations"] = process_melody_for_visualization(music.melody);
}