import './App.css';
import React, { Component, useEffect, useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from "axios";
import { useReactMediaRecorder } from "react-media-recorder";


function App() {

  var [code, setCode] = useState('hello world!');
  var [output, setOutput] = useState('output');
  var [ind, setInd] = useState(parseInt(0));
  var [resp, setResp] = useState({});
  var [displayText, setDisplayText] = useState("");
  var [newCode, setNewCode] = useState("");
  const [language, setLanguage] = useState('');
  const [isActive, setIsActive] = useState(false);

  var {
    status,
    startRecording,
    stopRecording,
    pauseRecording,
    mediaBlobUrl
  } = useReactMediaRecorder({
    video: false,
    audio: true,
    echoCancellation: true
  });

  console.log("url", mediaBlobUrl);

  var { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });

  useEffect(() => {
    setDisplayText(transcript);
  }, [transcript]);

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Brower doesnt support speech</span>;
  }

  const executeCode = async (programString) => {

    var select = document.getElementById('language_picker');
    var lang = select.options[select.selectedIndex].value;
    console.log("CODE IS", programString.code);
    const header = {
      'Content-Type': 'application/json'
    }
    console.log("Here lang is : ", lang)
    try {
      var lang2;
      if (lang == "cpp")
        lang2 = "cpp"

      else
        lang2 = "py"

      const response = await axios.post('https://api.codex.jaagrav.in', {
        code: programString.code,
        language: lang2                              // cplusplus - cpp, python -py
      }, { headers: header })

      if (response.data.output != '') {
        setOutput(response.data.output);
      }
      else {
        setOutput(response.data.error);
      }
      console.log(response)
    } catch (err) {
      console.log(err);
    }
  }

  const sendString = async () => {

    console.log('sending string');

    var select = document.getElementById('language_picker');
    var lang = select.options[select.selectedIndex].value;
    setLanguage(lang);
    console.log("Lang is :", language);

    if (lang == "nothing") {
      alert("please pick a language first!");
      return;
    }

    const response = await axios.post('http://127.0.0.1:5000/acceptString', {
      string: transcript,  //add 'transcript' for actual sentence
      language: lang,
      indentation: ind
    });

    setResp(response);

    console.log(response.data);

    if (response.data.code != null) {

      console.log(typeof (response.data.indentation));
      //code == "hello world!" ? setCode(response.data.code) : setCode(code + response.data.code);
      ind = setInd(response.data.indentation);
      console.log(ind);
      setNewCode(response.data.code);
    }

    else {
      console.log("got null");
    }

    setDisplayText("code: " + response.data.code);
    console.log("setting diplay text");
    //resetTranscript();
  }

  const sendAudio = async () => {
    console.log('sending audio to backend')

    var fd = new FormData();
    console.log("going to append this " + mediaBlobUrl)
    let blob = await fetch(mediaBlobUrl).then(r => r.blob());
    fd.append("audio_data", blob, "audio.wav");

    var url = 'http://127.0.0.1:5000/acceptAudio';
    fetch(url, {
      mode: "cors",
      method: "post",
      body: fd
    });
  }


  const acceptCode = () => {
    code == "hello world!" ? setCode(newCode) : setCode(code + newCode);
    resetTranscript();
    setDisplayText("");
  }

  return (

    <div className='h-screen w-screen'>

      {/* <div className='m-5 w-fit rounded-md p-2 text-white bg-orange-600 text-lg'> Language pick </div>
       */}

      <div className="m-3 xl:w-96">
        <select className="form-select appearance-none block w-1/2 px-3 py-1.5 text-base font-normal text-white
      bg-gray-800 bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded
      transition ease-in-out m-0
     focus:border-blue-600 focus:outline-none" aria-label="Default select example" id="language_picker">
          <option selected value="nothing">Select Language</option>
          <option value="cpp">C++</option>
          <option value="python">Python</option>
          <option value="java">Java</option>
        </select>
      </div>
      <div className='grid grid-cols-6 m-5 h-screen'>

        <textarea className='col-span-4 p-2 h-4/5 bg-blue-900 text-white' onChange={(e) => { setCode(e.target.value) }} value={code || " "} />

        <div className='col-span-2'>

          <div className='flex justify-center'>
            {/* <div className='ml-5 w-100 h-fit p-5 rounded-full bg-green-600 text-white hover:bg-green-500' onClick={SpeechRecognition.startListening}> Listen </div>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-red-600 text-white hover:bg-red-500' onClick={SpeechRecognition.stopListening}> Stop </div> */}
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-green-600 text-white hover:bg-green-500' onClick={() => {
              if (!isActive) {
                startRecording();
              }
              else {
                pauseRecording();
              }

              setIsActive(!isActive)
            }}> Start </div>

            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-red-600 text-white hover:bg-red-500' onClick={() => {
              stopRecording();
              pauseRecording();
              sendAudio();
            }}> Stop </div>

          </div>

          <div className='h-5'>
            {" "}
            <video src={mediaBlobUrl} controls />
          </div>

          <textarea className='m-5 p-2 h-1/6 w-10/12 bg-blue-200 text-black' onChange={(e) => { setDisplayText(e.target.value); setNewCode(e.target.value) }} value={displayText} />

          <div className='flex justify-center'>
            <div className='m-2 p-2 bg-blue-900 text-white w-fit hover:bg-blue-800' onClick={() => sendString()}>
              Process
            </div>
            <div className='m-2 p-2 bg-blue-900 text-white w-fit hover:bg-blue-800' onClick={() => acceptCode()}>
              Accept
            </div>
          </div>

          <div className='m-5 p-2 mx-auto bg-orange-500 text-white w-fit' onClick={() => executeCode({ code })}>
            Execute
          </div>

          <textarea className='m-5 p-2 h-1/4 w-10/12 bg-blue-300 text-black' value={output} />
        </div>

      </div>

    </div>

  );
}

export default App;
