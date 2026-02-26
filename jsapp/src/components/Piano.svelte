<script>
    import PianoUi from './PianoUI_source.svelte';


    let startingKey = 1
    let keyCount = 88
    let height = '100%'
    let width = '100%'
    let showNoteLabels = true
    let showHighlightKeys = false
    let highlightKeys = []
    let onKeyPress = (e) => {
    }
    let onKeyUnpress = (e) => {
        lastNoteSounded = e.currentTarget.getAttribute('data-note');
    }

    let lastNoteSounded = $state("none so far")
</script>


<div style="height: 420px; width: 100%; border: solid 5px gray; box-sizing: border-box;">
    <PianoUi
            starting_key={startingKey}
            key_count={keyCount}
            height={height}
            width={width}
            show_note_labels={showNoteLabels}
            show_highlight_keys={showHighlightKeys}
            highlight_keys={highlightKeys}
            on_key_press={onKeyPress}
            on_key_unpress={onKeyUnpress}
    />
</div>
<text>Last note sounded: {lastNoteSounded}</text>