# HarmonAI

HarmonAI is a visual analytics tool for exploring AI-generated harmonizations of a melody.
You load a melody, let an AI model ([AutoHarmonizer](https://arxiv.org/abs/2112.11122)) generate many chord accompaniments for it, and then compare those harmonizations using music-theory metrics, a piano roll, a harmonic lead sheet, and a circle of fifths.

> **This is the `Adjustments` branch, the current and recommended version of HarmonAI.**
> The `main` branch has an older state of the project.

---

## Contents

- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup](#setup)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Install the frontend](#2-install-the-frontend)
  - [3. Set up the calculation server](#3-set-up-the-calculation-server)
  - [4. Set up the AI model server](#4-set-up-the-ai-model-server)
- [Running HarmonAI](#running-harmonai)
- [Using HarmonAI](#using-harmonai)
- [Repository structure](#repository-structure)
- [Deploying the frontend to GitHub Pages](#deploying-the-frontend-to-github-pages)
- [Troubleshooting](#troubleshooting)

---

## Architecture

HarmonAI has three parts that run at the same time:

| Part | Tech | Location | Address |
|---|---|---|---|
| **Frontend** | Svelte 5 + Vite, LineUp.js, D3, Magenta | `jsapp/` | http://localhost:5173/HarmonAI/ |
| **Calculation server** | Flask, music21 (Python 3.10.2) | `backend/calculations/` | http://127.0.0.1:5000 |
| **AI model server** | Flask, TensorFlow/Keras, AutoHarmonizer (Python 3.7.9) | `backend/aimodel/` | http://127.0.0.1:5555 |

- The **calculation server** parses uploaded melodies (MusicXML/MIDI), computes the harmonization metrics, and exports selected harmonizations as MusicXML + MIDI.
- The **AI model server** runs AutoHarmonizer and generates harmonizations of the melody at different harmonic rhythm densities.

The two servers need **different Python versions**, so each one gets its own virtual environment.

---

## Requirements

- **Windows**. The helper scripts (`run_backend_*.bat`) are Windows batch files. On other platforms, run the commands in them manually.
- **Node.js 18.12.1** (newer LTS versions will probably work too)
- **Python 3.10.2** for the calculation server
- **Python 3.7.9** for the AI model server
- **7-Zip** (or a similar tool) to extract the split model-weights archive
- Optional: an NVIDIA GPU with CUDA for faster generation. TensorFlow also runs on the CPU, but more slowly.

> Tip: install both Python versions side by side and use the [Python launcher](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) (`py -3.10`, `py -3.7`) to pick the right one.

---

## Setup

All commands below run in **cmd** from the repository root unless stated otherwise.

### 1. Clone the repository

```cmd
git clone https://github.com/snrau/HarmonAI.git
cd HarmonAI
git checkout Adjustments
```

### 2. Install the frontend

Install the dependencies in the repository root (for the helper scripts) **and** in `jsapp/` (for the app itself):

```cmd
npm install
cd jsapp
npm install
cd ..
```

### 3. Set up the calculation server

The batch script expects the virtual environment to be called `cvenv` and to be inside `backend\calculations\`:

```cmd
cd backend\calculations
py -3.10 -m venv cvenv
cvenv\Scripts\activate
pip install -r requirements.txt
deactivate
cd ..\..
```

### 4. Set up the AI model server

#### 4.1 Create the virtual environment

The batch script expects the virtual environment to be called `aivenv` and to be inside `backend\aimodel\`:

```cmd
cd backend\aimodel
py -3.7 -m venv aivenv
aivenv\Scripts\activate
pip install -r requirements.txt
pip install flask
deactivate
```

> `requirements.txt` does not include Flask, so install it separately as shown above.
> `newreq.txt` is a fully pinned dependency snapshot for reference only. It contains packages (for example `numpy==2.2.6`) that cannot be installed on Python 3.7.

#### 4.2 Extract the model weights

The pretrained weights are stored as a **split zip archive** (`weights.zip` + `weights.z01`) because of GitHub's file size limit. Extract them so that `weights.hdf5` is directly inside `backend\aimodel\`:

- With 7-Zip in Explorer: right-click `weights.zip` → *7-Zip* → *Extract Here*
- Or from the command line:
  ```cmd
  "C:\Program Files\7-Zip\7z.exe" x weights.zip
  ```

Afterwards the folder should contain `backend\aimodel\weights.hdf5`.

#### 4.3 Create the working folders

The model server writes the current melody into `inputs\` and the generated harmonizations into `outputs\`. These folders are git-ignored, so create them once:

```cmd
mkdir inputs outputs
cd ..\..
```

> You only need `data_corpus.zip` and `dataset/` to **retrain** the model (see [backend/aimodel/README.md](backend/aimodel/README.md)). They are not needed to run HarmonAI.

---

## Running HarmonAI

Start everything (both servers + frontend) with one command from the repository root:

```cmd
npm start
```

Then open **http://localhost:5173/HarmonAI/** in your browser.

You can also start the parts separately, each in its own terminal:

| Command | Starts |
|---|---|
| `npm run frontend` | Vite dev server (frontend) |
| `npm run backend` | both Python servers |
| `npm run calc` | calculation server only (`run_backend_calc.bat`) |
| `npm run model` | AI model server only (`run_backend_model.bat`) |

---

## Using HarmonAI

### 1. Load a melody

Use the buttons in the menu:

| Button | Action |
|---|---|
| **Upload file** | Upload your own melody (`.mxl`, `.xml`, `.musicxml`, `.mid`, `.midi`). Uploaded files are stored in `input/`. |
| **Get melody** | Loads the default melody (`input/brahms_inspired_transposed_to_some_sharps.mxl`) from the calculation server. |
| **Get vinci melody** | Loads a built-in example melody that needs no server. |

The `input/` folder has more example melodies you can upload.

### 2. Get harmonizations

| Button | Action |
|---|---|
| **Generate Harmonizations with AI** | Sends the melody to AutoHarmonizer. It generates harmonizations over a range of rhythm densities (0 → 1) and keeps only distinct results. **This can take a while, so wait until the views update.** |
| **Get Existing Har** | Loads all harmonizations that are already in `backend/aimodel/outputs/` without running the model again. |
| **Get Vinci Example** | Loads precomputed example harmonizations for the vinci melody. No AI server needed. |

The metrics are computed automatically on the calculation server after the harmonizations load.

> To try the tool quickly without the AI server, use **Get vinci melody** + **Get Vinci Example**. You only need the calculation server for that.

### 3. Explore and compare

- **LineUp table**: one row per harmonization. You can sort, filter, and weight them by metrics, including:
  - `CC`: chord coverage
  - `CHE`: chord histogram entropy
  - `CTD`: chord tonal distance
  - `CTnCTR`: chord tone to non-chord tone ratio
  - `PCS`: pitch consonance score
  - `MCTD`: melody–chord tonal distance
  - `rythm_density`: the harmonic rhythm density used for generation
  - Roman numerals, chord-tone class progressions, typicality of chord transitions, and key

  Most metrics follow Yeh et al.; see `backend/calculations/metrics_based_on_yeh_et_al.py`.
- **Piano roll**: shows the melody together with the chords of the selected harmonization(s), colored by harmonic function.
- **Harmonic lead sheet**: a lead-sheet style view of the chord progressions.
- **Circle of fifths**: shows the harmonic movement of the selected harmonizations.

Select rows in the LineUp table to highlight those harmonizations in the other views.

### 4. Export

Select one or more harmonizations and click **Save selected harmonization(s)**. You get a `score.zip` file with the melody and the selected harmonizations as **MusicXML** and **MIDI**.

---

## Repository structure

```
HarmonAI/
├── jsapp/                     # Svelte frontend
│   └── src/
│       ├── App.svelte
│       ├── components/        # LineUp, PianoRoll, CircleOfFifths, Harmonic_Leadsheet, ...
│       └── helper/            # server communication, coloring, music utilities, examples
├── backend/
│   ├── calculations/          # Flask server: melody parsing, metrics, export   (port 5000)
│   └── aimodel/               # Flask server: AutoHarmonizer model             (port 5555)
├── input/                     # example melodies / uploaded melodies
├── output/                    # example harmonized pieces
├── run_backend_calc.bat       # starts the calculation server in its venv
├── run_backend_model.bat      # starts the AI model server in its venv
└── package.json               # npm scripts (start, frontend, backend, calc, model)
```

---

## Deploying the frontend to GitHub Pages

The Vite config uses `base: '/HarmonAI/'` for GitHub Pages hosting:

```cmd
cd jsapp
npm run build
npm run deploy
```

This publishes `jsapp/dist` to the `gh-pages` branch.

> Note: the frontend calls the backends at `http://127.0.0.1:5000` and `http://127.0.0.1:5555`, so the hosted version also needs both servers running **locally**. To use a remotely hosted calculation server instead, change `serverAddressCalc` in `jsapp/src/helper/servercomms.js`. The calculation server includes a `Procfile`/`runtime.txt` for hosting with gunicorn.

---

## Troubleshooting

**"No matching export in … for import …" errors from LineUp.js**
Some redundant imports inside `node_modules/lineupjs` caused these errors. I fixed them by removing those imports from the lineupjs files in `node_modules`. `vite.config.js` also aliases `lineupjs` to `lineupjs/build/LineUpJS.js`, which should avoid the problem. If the errors still appear after a fresh `npm install`, remove the redundant imports again.

**Nothing happens when clicking a button**
One of the servers is probably not running, or it crashed. Error handling in the frontend is minimal, so check the terminal output of the servers and the browser console.

**The AI server fails to start / cannot find `weights.hdf5`**
Make sure you extracted the weights (step 4.2) into `backend\aimodel\` and that the `inputs\` and `outputs\` folders exist (step 4.3).

**Keras / TensorFlow version conflicts**
`requirements.txt` does not pin Keras. If Keras does not match TensorFlow 2.10, install the matching version with `pip install keras==2.10.0`.

**The batch scripts cannot find the venv**
The scripts look for `backend\calculations\cvenv` and `backend\aimodel\aivenv`. Use exactly these names and locations.

**"Get Existing Har" shows old harmonizations**
`backend/aimodel/outputs/` keeps the results of all previous generations. Empty that folder to start fresh.

---

## Credits

- AI harmonization model: **AutoHarmonizer**, *Generating Chords from Melody with Flexible Harmonic Rhythm and Controllable Harmonic Density* ([arXiv:2112.11122](https://arxiv.org/abs/2112.11122)). See [backend/aimodel/README.md](backend/aimodel/README.md) and [backend/aimodel/LICENSE](backend/aimodel/LICENSE).
- Metrics are based on Yeh et al.
- Visualization: [LineUp.js](https://lineup.js.org/), [D3](https://d3js.org/), [Magenta.js](https://magenta.tensorflow.org/js)
