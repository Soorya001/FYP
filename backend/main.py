import json
from flask import Flask, request, jsonify
import phraseToCode as Converter
app = Flask(__name__)


# API to check if backend is up and running.
@app.route("/check-backend-api")
def members():
    return {"members": ["member1","member2","member3","member4","member5"]}

@app.route('/acceptString',methods=['POST'])
def acceptString():
    stringReceived = request.json.get('string')
    language = request.json.get('language')

    # string is the key name of the identified string
    # language - lang to be converted to.
    # POST request must contain the following- { stringtoSend, ProgLanguage}

    convertedCode =  Converter.extract_keywords(stringReceived, language)  
    # This converts the input command- stringReceived, to its equivalent cpp or python code and returns it as a string.

    return {"code":convertedCode}    #Returns the converted Code


if __name__ == "__main__":
    app.run(debug=True)

