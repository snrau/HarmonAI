<script>
    import {music} from "../state.svelte.js";

    async function saveSelectedHarmonizations() {
        if (music.selected_harmonizations.length === 0) {
            alert("No harmonization selected.");
        } else {
            //FIXME error handling when server response is in some way (most often either server is not running or internal server error due to bug in my code) failing + communication to user
            const response = await fetch('http://127.0.0.1:5000/save_harmonizations', {
                method: 'POST',
                body: JSON.stringify({
                    "harmonizations": music.selected_harmonizations,
                    "melody": music.melody,
                    "path": "E:/Users/Verena/Documents/Studium/Master/Thesis/Code/HarmonAI/save_harmonizations/", // TODO let user pick these values
                    "filename": "some_piece"
                }),
                headers: {
                    "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
                    "Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
                    "Content-Type": "application/json", // this shows the expected content type
                    "Access-Control-Allow-Origin": "*"
                }
            });
            // TODO inform user of successful saving
            document.getElementById("messages_div").innerHTML = "Saved harmonizations";
        }
    }
</script>

<button id="btn-saveSelectedHarmonizations" class="button_class" onclick={saveSelectedHarmonizations}>
    Save selected harmonization(s)
</button>

<style>
    button {
        background-color: #999;
    }
</style>