# HarmonAI

> ## ⚠️ Use the [`Adjustments`](https://github.com/snrau/HarmonAI/tree/Adjustments) branch
>
> The `main` branch has an **older, outdated state** of HarmonAI.
> The current version is on the **[`Adjustments`](https://github.com/snrau/HarmonAI/tree/Adjustments)** branch. It has all recent features, fixes, and the full setup and usage guide.

HarmonAI is a visual analytics tool for exploring AI-generated harmonizations of a melody. It combines the AutoHarmonizer model with metric-based comparison views (LineUp table, piano roll, harmonic lead sheet, circle of fifths).

## Getting the current version

```cmd
git clone https://github.com/snrau/HarmonAI.git
cd HarmonAI
git checkout Adjustments
```

If you already cloned the repository:

```cmd
git fetch
git checkout Adjustments
```

Then follow the setup instructions in the [`Adjustments` README](https://github.com/snrau/HarmonAI/blob/Adjustments/README.md).

## What `Adjustments` has that `main` doesn't

- Coloring of chords by harmonic function, with a legend
- Selection and coloring linked across the piano roll and the other views
- A circle-of-fifths view
- Reworked ordering of harmonizations and new LineUp columns (key, chord colors, typicality of chord transitions)
- Upload of your own melodies (MusicXML / MIDI)
- A new built-in example melody with harmonizations
- Adjustments for hosting the frontend on GitHub Pages
- Full setup and usage documentation
