import os.path

import flask
from flask import Flask, send_from_directory, jsonify, request, Response
import random
import tempfile
import zipfile
import io
import os


from converter import json_to_music21, get_melody_from_mxl, score_to_musicxml_string
from metrics_management import calculate_metrics, get_note_ranges
from variations_within_chords import generate_variations_within_chords
from werkzeug.utils import secure_filename

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




# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../../jsapp/public', path)


UPLOAD_FOLDER = "../../input/"

@app.route("/melody")
def getMelody():
    filepath = None

    # ✅ Case 1: file uploaded
    if "file" in request.files:
        file = request.files["file"]

        if file.filename != "" :
            filename = secure_filename(file.filename)

            # avoid overwriting
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)

    # ✅ Case 2: fallback to hardcoded file
    if filepath is None:
        filepath = os.path.join(
            UPLOAD_FOLDER,
            "brahms_inspired_transposed_to_some_sharps.mxl"
        )
    # ✅ Your existing logic
    melody = get_melody_from_mxl(os.path.dirname(filepath), os.path.basename(filepath))

    return jsonify(melody)


@app.route("/save_harmonizations", methods=['POST'])
def saveHarmonizations():
    music_data_json = {}
    music_data_json["melody"] = request.json["melody"]
    music_data_json["harmonizations"] = request.json["harmonizations"]
    score = json_to_music21(music_data_json)

    #xml_string = score_to_musicxml_string(score)

    # ✅ Create temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        xml_path = os.path.join(tmpdir, "score.musicxml")
        midi_path = os.path.join(tmpdir, "score.mid")

        # ✅ Write both formats
        score.write("musicxml", xml_path)
        score.write("midi", midi_path)

        # ✅ Create ZIP in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            zf.write(xml_path, "score.musicxml")
            zf.write(midi_path, "score.mid")

        memory_file.seek(0)
    #return jsonify({"status": 201})
    return Response(
        memory_file,
        mimetype="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=score.zip"
        }
    )


@app.route("/metrics", methods=['POST'])
def provideMetrics():
    music_data_json = request.json
    harmonizations_json = music_data_json["harmonizations"]
    # melody_json = music_data_json["melody"]

    # first convert to music21 representation
    music_data_music21 = json_to_music21(music_data_json)

    harmonizations_with_variations = generate_variations_within_chords(
        music_data_music21,
        harmonizations_json
    )

    # then hand over to a metrics calculation management script, that has access to all metric functions
    # that script saves the results in the representation? since that is possible for both...
    harmonizations_and_metrics = calculate_metrics(music_data_music21, harmonizations_with_variations, None)

    # convert back to json table including all the calculated data
    # currently not needed, since all is directly put in the harmonizations_json dict

    # no need to convert the melody back since we have that already in needed format

    meta_data = get_note_ranges(music_data_music21)

    return jsonify({"harmonizations": harmonizations_and_metrics, "melody": music_data_json["melody"], "meta": meta_data})


@app.route("/singleMetrics", methods=['POST'])
def provideSingleMetrics():
    music_data_json = request.json
    harmonizations_json = music_data_json["harmonizations"]
    key = music_data_json["key"]
    
    # melody_json = music_data_json["melody"]

    # first convert to music21 representation
    music_data_music21 = json_to_music21(music_data_json)

    # then hand over to a metrics calculation management script, that has access to all metric functions
    # that script saves the results in the representation? since that is possible for both...
    harmonizations_and_metrics = calculate_metrics(music_data_music21, harmonizations_json, key)

    meta_data = get_note_ranges(music_data_music21)

    return jsonify({"harmonization": harmonizations_and_metrics, "meta": meta_data})




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
