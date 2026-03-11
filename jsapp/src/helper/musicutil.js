import * as mm from "@magenta/music";
import { music } from "../state.svelte.js";
import { run } from "svelte/legacy";

let magentaPlayer = null;

let playTimeout = null

const instrument = 2

export async function playHarmonization(row) {
    const data = row.v
    const index = row.i
    //console.log(music.playing_index, index)
    if (music.playing_index === index) {
        clearTimeout(playTimeout)
        magentaPlayer.stop();
        music.playing_index = -1
        highlightPlayingRow(-1)
    } else {
        const events = data.midiplayback;

        // Stop existing playback
        if (magentaPlayer) {
            magentaPlayer.stop();
        } else {
            //magentaPlayer = new mm.SoundFontPlayer("https://storage.googleapis.com/magentadata/js/soundfonts/salamander")
            magentaPlayer = new mm.SoundFontPlayer("https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus")
            await magentaPlayer.loadAllSamples(instrument);
        }

        music.playing_index = index
        highlightPlayingRow(index)
        clearTimeout(playTimeout)

        // Play the notes
        let seq = {
            notes: data.midiplayback,
            totalLength: Math.max(...data.midiplayback.map(v => v.endTime)),
            tempos: [{ qpm: 120 }],
        }
        changeInstrument(seq, instrument);
        magentaPlayer.start(seq)

        playTimeout = setTimeout(() => {
            console.log("Playback finished");

            music.playing_index = -1;
            highlightPlayingRow(-1);
            magentaPlayer.stop();
        }, seq.totalLength * 1000 + 200);
    }
}

export function highlightPlayingRow(index) {
    console.log("highlighting row", index)
    document
        .querySelectorAll(".le-tr")
        .forEach(r => r.classList.remove("playing"));

    if (index === -1) return;

    const row = document.querySelector(`.le-tr[data-i="${index}"]`);
    if (row) row.classList.add("playing");
}


function changeInstrument(seq, program) {
    seq.notes.forEach(n => {
        n.program = program;
        n.instrument = 0;
    });
}