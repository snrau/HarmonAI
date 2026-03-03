import * as mm from "@magenta/music";
import { music } from "../state.svelte.js";

let magentaPlayer = null;

let currentlyPlayed = -1

export function playHarmonization(row) {
    const data = row.v
    const index = row.i
    console.log(music.playing_index, index)
    if (music.playing_index === index) {
        magentaPlayer.stop();
        music.playing_index = -1
    } else {
        const events = data.midiplayback;

        // Stop existing playback
        if (magentaPlayer) {
            magentaPlayer.stop();
        } else {
            magentaPlayer = new mm.SoundFontPlayer("https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus")
        }

        music.playing_index = index

        // Play the notes
        let seq = {
            notes: data.midiplayback,
            totalLength: Math.max(...data.midiplayback.map(v => v.endTime)),
            tempos: [{ qpm: 120 }],
        }

        console.log(seq)

        magentaPlayer.start(seq).then(() => {
            music.playing_index = -1
            magentaPlayer.stop()
        });
    }
}