import './App.css';
import React, { Component, useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from "axios";

function App() {

  const [code, setCode] = useState('hello world!');
  const [output, setOutput] = useState('output');
  const [ind, setInd] = useState(parseInt(0));

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Brower doesnt support speech</span>;
  }

  const sendString = async () => {

    console.log('sending string');

    var select = document.getElementById('language_picker');
    var lang = select.options[select.selectedIndex].value;
    console.log(lang);

    if (lang == "nothing") {
      alert("please pick a language first!");
      return;
    }

    const response = await axios.post(' http://127.0.0.1:5000/acceptString', {
      string: "include headerfile pandas",
      language: lang,
      indentation: ind
    });

    console.log(response.data);

    if (response.data.code != null) {
      console.log(typeof(response.data.indentation));
      code == "hello world!" ? setCode(response.data.code) : setCode(code + response.data.code);
      ind = (setInd(parseInt(response.data.indentation)));
      console.log(ind);
    }

    else {
      console.log("got null");
    }

    resetTranscript();
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

        <textarea className='col-span-4 p-2 h-4/5 bg-blue-900 text-white' value={code || " "} />

        <div className='col-span-2'>

          <div className='flex justify-center'>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-green-600 text-white hover:bg-green-500' onClick={SpeechRecognition.startListening}> Listen </div>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-red-600 text-white hover:bg-red-500' onClick={SpeechRecognition.stopListening}> Stop </div>
          </div>

          <div className='m-5 p-2 h-1/6 w-10/12 bg-blue-200 text-black'> {transcript} </div>


          <div className='m-2 p-2 bg-blue-900 text-white w-fit mx-auto hover:bg-blue-800' onClick={() => sendString()}>
            Accept
          </div>


          <div className='m-5 p-2 mx-auto bg-orange-500 text-white w-fit'>
            Execute
          </div>

          <div className='m-5 p-2 h-1/4 w-10/12 bg-blue-300 text-black'> {output} </div>

        </div>

      </div>

    </div>

  );
}

export default App;
