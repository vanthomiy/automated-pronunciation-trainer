import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from sound_handler import NoiseAdder
from user_handler import UserHandler
from whisper_transcriptor import WhisperTranscriptor

app = Flask(__name__)
CORS(app)

app.config['transcriptor'] = WhisperTranscriptor()
app.config['noise'] = NoiseAdder('output.mp3')


@app.route('/api/login/<user_name>')
def login(user_name):
    app.config['user'] = UserHandler.get_user(user_name)
    return "true"


@app.route('/api/set_model/<model_name>')
def set_model(model_name):
    app.config['transcriptor'] = WhisperTranscriptor(model_name)
    return "true"


@app.route('/api/models')
def get_models():
    return jsonify(WhisperTranscriptor.get_models())


@app.route('/api/next')
def next():
    # delete output.mp3 if it exists
    if os.path.exists("./output.mp3"):
        os.remove("./output.mp3")
    return app.config['user'].get_text()


@app.route('/api/history')
def history():
    history_data = jsonify(app.config['user'].history)
    return history_data


@app.route('/api/user')
def user():
    user_data = jsonify(app.config['user'].create_user_json())
    return user_data


@app.route('/api/user/change_level/<level>')
def change_level(level):
    app.config['user'].user_level = int(level)
    app.config['user'].save()
    return "true"


@app.route('/api/get_record/')
def get_record():
    """
    send byte array (audio_data) to frontend
    :return:
    """
    try:
        # get byte array from wav file
        byte_array = app.config['noise'].get_noise_array("output.mp3")
        # convert byte array to byte string
        byte_string = bytes(byte_array)
        # send byte string to frontend
        return byte_string
    except Exception as e:
        print(e)
        return "-1"

@app.route('/api/send_record/', methods=['POST'])
def send_record():
    """
    receive byte array (audio_data) from frontend and save it as wav file
    :param audio_data:
    :return:
    """
    try:
        # get byte string from request.data
        byte_string = request.data
        # convert byte string to byte array
        byte_array = bytearray(byte_string)
        # do something with byte_array
        # save byte_array as mp3 file using pydub
        app.config['noise'].save_file(byte_array)

        # add noise to wav file
        app.config['noise'].add_noise()
        print("noise added")
        text = app.config['transcriptor'].transcript()
        print("transcripted")
        score, alignment = app.config['user'].add_history(text)
        print("history added")

        return jsonify({"score": score, "text": alignment})
    except Exception as e:
        print(e)
        return "-1"


@app.route('/api/noise')
def get_noise():
    keys = list(app.config['noise'].noises.keys())
    return jsonify(keys)


@app.route('/api/set_noise/<noise>')
def set_noise(noise):
    app.config['noise'].selected_noise = noise
    if noise == "None":
        return None
    wf = app.config['noise'].get_noise_array()
    return wf


if __name__ == '__main__':
    app.run()
