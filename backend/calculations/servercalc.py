import os.path

import flask
from flask import Flask, send_from_directory, jsonify, request
import random

from converter import json_to_music21, get_melody_from_mxl
from metrics_management import calculate_metrics, get_note_ranges
from variations_within_chords import generate_variations_within_chords

app = Flask(__name__)


# put this sippet ahead of all your blueprints
# blueprint can also be app~~
@app.after_request
def after_request(response):
    header = response.headers
    # for some reason it does not work with the 'http://localhost:5173/' instead of the wildcard
    header['Access-Control-Allow-Origin'] = '*'

    header['Access-Control-Allow-Headers'] = "*"
    header["Access-Control-Allow-Methods"] = 'OPTIONS,POST,GET'
    # Other headers can be added here if needed
    return response


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('/', 'Test_datensatz_LineUp.json')


@app.route("/static_test_Data_from_code")
def test():
    return flask.jsonify([["label1", "label2"], [1, 2], [[1, 1, 1], [2, 2, 2]]])


@app.route("/lineupjs-sourcemap-file")
def provide_lineupjs_sourcemap_file():
    return flask.send_file(
        "./lineup_sourcemap_files/LineUpJS.js")


@app.route("/lineupcss-sourcemap-file")
def provide_lineupcss_sourcemap_file():
    return flask.send_file(
        "./lineup_sourcemap_files/LineUpJS.css")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../../fronted/public', path)


@app.route("/rand/")
def hello():
    return str(random.randint(0, 100))


@app.route("/melody")
def getMelody():
    # TODO implement better solution than "somewhere hidden in the code" hardwire local file paths...
    melody = get_melody_from_mxl("../../input/",
                                 "brahms_inspired_transposed_to_some_sharps.mxl")
    return jsonify(melody)


@app.route("/save_harmonizations", methods=['POST'])
def saveHarmonizations():
    music_data_json = {}
    music_data_json["melody"] = request.json["melody"]
    music_data_json["harmonizations"] = request.json["harmonizations"]
    score = json_to_music21(music_data_json)

    score.write('mxl', fp=os.path.join(request.json["path"], request.json["filename"]))

    return jsonify({"status": 201})


@app.route("/metrics", methods=['POST'])
def provideMetrics():
    music_data_json = request.json
    harmonizations_json = music_data_json["harmonizations"]
    # melody_json = music_data_json["melody"]

    # first convert to music21 representation
    music_data_music21 = json_to_music21(music_data_json)

    # then hand over to a metrics calculation management script, that has access to all metric functions
    # that script saves the results in the representation? since that is possible for both...
    harmonizations_and_metrics = calculate_metrics(music_data_music21, harmonizations_json)

    # convert back to json table including all the calculated data
    # currently not needed, since all is directly put in the harmonizations_json dict

    # no need to convert the melody back since we have that already in needed format

    meta_data = get_note_ranges(music_data_music21)

    return jsonify({"harmonizations": harmonizations_and_metrics, "melody": music_data_json["melody"], "meta": meta_data})


@app.route("/variations_within_chords", methods=['POST'])
def provideVariationsWithinChords():
    music_data_json = request.json
    harmonizations_json = music_data_json["harmonizations"]

    # first convert to music21 representation
    music_data_music21 = json_to_music21(music_data_json)

    # then hand over to a metrics calculation management script, that has access to all metric functions
    # that script saves the results in the representation? since that is possible for both...
    harmonizations_with_variations_json = generate_variations_within_chords(music_data_music21, harmonizations_json)

    # convert back to json table including all the calculated data
    # currently not needed, since all is directly put in the harmonizations_json dict

    # no need to convert the melody back since we have that already in needed format


    return jsonify({"harmonizations": harmonizations_with_variations_json, "melody": music_data_json["melody"]})


if __name__ == "__main__":
    app.run(debug=True)
