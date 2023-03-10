from speechbrain.pretrained import EncoderDecoderASR
import speechbrain as sb
from base64 import b64decode
from io import StringIO
import phraseToCode as Converter
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import json
import sys
import requests


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"
headers = {"Authorization": "Bearer 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"}


def clean_text(text):

    # removing a full stop if present
    if text[-1] == '.':
        text = text[:-1]

    # making evething small case for better processing
    text = text.lower()
    return text


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


sys.path.append('D:\fyp\FYP\backend\speech\speechbrain')

# asr_model = EncoderDecoderASR.from_hparams(
#     source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")


asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="F:\save-20230308T062600Z-002\save\CKPT+2023-03-07+19-14-24+00")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# API to check if backend is up and running.


@app.route("/check-backend-api")
def members():
    return json.dumps({"members": ["Jayasooryan", "Madhava Prashath"]})


@app.route('/acceptAudio', methods=['POST'])
def acceptAudio():

    try:
        print(request.files)
        audio = request.files['audio_data']
        print(audio)
        audio.save('F:/audio.mp3')

        print('received audio file', type(audio), sys.getsizeof(audio))

        text = asr_model.transcribe_file('F:/audio.mp3')
        print(text)

        # text = query('F:/audio.mp3')['text']

        text = clean_text(text)

        audio.flush()
        audio.close()

        return json.dumps({"received": text})

    except:
        return json.dumps({"reviced": "ERRORONOUS AUDIO"})


@app.route('/acceptString', methods=['POST'])
def acceptString():
    stringReceived = request.json.get('string')
    language = request.json.get('language')
    indentation = request.json.get('indentation')

    # string is the key name of the identified string
    # language - lang to be converted to.
    # POST request must contain the following- { stringtoSend, ProgLanguage}

    print('data received: ', stringReceived, ' language: ',
          language, ' current indentation: ', indentation)

    # This converts the input command- stringReceived, to its equivalent cpp or python code and returns it as a string.

    convertedCode, indentation = Converter.extract_keywords(
        stringReceived, language, indentation)

    print("updated indentation: ", indentation)

    oldCode = convertedCode

    convertedCode = (indentation * ("\t")) + convertedCode

    if (oldCode == "{\n"):
        indentation += 1

    # Returns the converted Code
    return json.dumps({"code": convertedCode, "indentation": indentation})


@app.route('/execute/python', methods=['POST'])
def execute_code():
    code = request.json['code']
    # exec func below directly prints the output in the console without returning. SO in oder to capture the output we temporarily change/assign the stdout to our own object and revert it later.
    old_stdout = sys.stdout
    temp = sys.stdout = StringIO()
    try:
        # exec(code)
        exec(code, {}, {'output': temp})
    except (SyntaxError) as syntaxError:
        return json.dumps({"code": "Syntax Error: "+syntaxError.msg+" at line: "+str(syntaxError.lineno)+"\n"})
    except (NameError) as nameError:
        return json.dumps({"code": "Name Error... \n"})
    finally:
        sys.stdout = old_stdout
    # get value fetches the actual output present in the temp object
    return json.dumps({"code": temp.getvalue()})


if __name__ == "__main__":
    app.run(debug=True)
