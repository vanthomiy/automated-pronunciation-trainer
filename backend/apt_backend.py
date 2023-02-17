import os
import time
import wave

from flask import Flask, jsonify
from flask_cors import CORS

from Praktikum2.backend.sound_handler import SoundRecorder, SoundPlayer, NoiseAdder
from Praktikum2.backend.user_handler import UserHandler
from Praktikum2.backend.whisper_transcriptor import WhisperTranscriptor

app = Flask(__name__)
CORS(app)

app.config['recorder'] = SoundRecorder('output.wav')
app.config['transcriptor'] = WhisperTranscriptor()
app.config['noise'] = NoiseAdder('output.wav')


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
    # delete output.wav if it exists
    if os.path.exists("./output.wav"):
        os.remove("./output.wav")
    return app.config['user'].get_text()


@app.route('/api/record')
def record():
    try:
        app.config['recorder'] = SoundRecorder('output.wav')
        started = app.config['recorder'].start()
        return "true" if started else "false"
    except Exception as e:
        print(e)
        return "false"


@app.route('/api/stop_record')
def stop_record():
    try:
        app.config['recorder'].stop()
        print("recording stopped")
        app.config['noise'].add_noise()
        print("noise added")
        text = app.config['transcriptor'].transcript()
        print("transcripted")
        score, alignment = app.config['user'].add_history(text)
        print("history added")
        # return score and text
        return jsonify({"score": score, "text": alignment})
    except Exception as e:
        print(e)
        return "-1"


@app.route('/api/cancel_record')
def cancel_record():
    try:
        app.config['recorder'].stop()
        return "true"
    except Exception as e:
        print(e)
        return "false"


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


@app.route('/api/noise')
def get_noise():
    keys = list(app.config['noise'].noises.keys())
    return jsonify(keys)


@app.route('/api/set_noise/<noise>')
def set_noise(noise):
    app.config['noise'].selected_noise = noise
    return "true"


@app.route('/api/play_noise/<command>/<is_recording>')
def play_noise(command, is_recording):
    if command == "play":
        wf = app.config['noise'].get_noise()
        if "True" == is_recording:
            wf = wave.open('./output.wav', 'rb')
        app.config['player'] = SoundPlayer(wf)
        app.config['player'].play = True
        result = app.config['player'].start()
        return "true" if result else "false"
    elif command == "stop":
        # stop playing noise
        app.config['player'].play = False
        app.config['player'].t.join()
    return "true"


if __name__ == '__main__':
    app.run()
