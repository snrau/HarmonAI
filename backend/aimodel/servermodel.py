import flask
from flask import Flask, send_from_directory, jsonify, request

from converter import construct_harmonies_table, provide_as_model_input
from harmonizer import *

app = Flask(__name__)

# Build harmonic rhythm and chord model
model = build_model(SEGMENT_LENGTH, RNN_SIZE, NUM_LAYERS, DROPOUT, WEIGHTS_PATH, training=False)

# put this sippet ahead of all your blueprints
# blueprint can also be app~~
@app.after_request
def after_request(response):
    header = response.headers
    # for some reason it does not work with the 'http://localhost:5173/' instead of the wildcard
    header['Access-Control-Allow-Origin'] = '*'

    # to enable receiving data (the melody and parameters)
    header['Access-Control-Allow-Headers'] = "*"
    header["Access-Control-Allow-Methods"] = 'OPTIONS,POST,GET'
    # Other headers can be added here if needed
    return response


@app.route("/autoharmonizer", methods=['POST'])
def get_harmonizations():
    melody_json = request.json["melody"]
    rhythm_density_lower_bound = request.json["rhythm_density_lower_bound"]
    rhythm_density_upper_bound = request.json["rhythm_density_upper_bound"]

    provide_as_model_input(melody_json)

    # Load data from 'inputs'
    filenames = get_filenames(input_dir=INPUTS_PATH)
    data_corpus = convert_files(filenames, fromDataset=False)
    

    seen = set()
    # Process each melody sequence
    for idx in trange(len(data_corpus)):
        melody_data = data_corpus[idx][0]
        beat_data = data_corpus[idx][1]
        key_data = data_corpus[idx][2]
        score = data_corpus[idx][3]
        filename = data_corpus[idx][4]

        densities = (
        list(range(int(rhythm_density_lower_bound * 100), int(rhythm_density_upper_bound * 100) + 1, 1))
        + list(range(0, int(rhythm_density_lower_bound * 100) + 1, 5))
    )

        # values for rhythm_density can be between 0 and 1
        for density in densities:
            rythm_density = density / 100

            chord_data = generate_chord(
                model, melody_data, beat_data, key_data, rhythm_gamma=rythm_density
            )

            # convert to hashable representation
            chord_key = tuple(chord_data)

            if chord_key in seen:
                continue

            seen.add(chord_key)

            filename_extended = filename[:-4] + f"_variant_{rythm_density}.mxl"
            export_music(score, beat_data, chord_data, filename_extended)

    return jsonify(construct_harmonies_table(get_filenames(input_dir=OUTPUTS_PATH)))


@app.route("/existing_harmonizations")
def get_existing_harmonizations():
    return jsonify(construct_harmonies_table(get_filenames(input_dir=OUTPUTS_PATH)))



if __name__ == "__main__":
    # set debug=False as well as threaded= False to circumvent some issue of keras 2.3.0 when using flask
    # without flask debug=True and threaded defaulting is running (as is done in harmonizer.py)
    app.run(port=5555, debug=False, threaded=False)
