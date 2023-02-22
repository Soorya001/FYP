from speechbrain.pretrained import EncoderDecoderASR
import speechbrain as sb
from base64 import b64decode
from io import StringIO
import phraseToCode as Converter
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import json
import sys
sys.path.append('D:\fyp\FYP\backend\speech\speechbrain')
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# API to check if backend is up and running.


@app.route("/check-backend-api")
def members():
    return json.dumps({"members": ["Jayasooryan", "Madhava Prashath"]})


@app.route('/acceptAudio', methods=['POST'])
def acceptAudio():

    print(request.files)
    audio = request.files['audio_data']
    print(audio)
    audio.save('F:/audio.wav')

    print('received audio file', type(audio), sys.getsizeof(audio))

    text = asr_model.transcribe_file('F:/audio.wav')

    audio.flush()
    audio.close()

    return json.dumps({"received": text})


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
