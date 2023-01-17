import logo from './logo.svg';
import './App.css';
import React, { Component, useState } from 'react';
import SpeechRecognition, {useSpeechRecognition} from 'react-speech-recognition';
import axios from "axios";

function App() {

  const [code, setCode] = useState('hello world!');

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Brower doesnt support speech</span>;
  }

  const sendString = async () => {

    console.log('sending string');

    const response = await axios.post(' http://127.0.0.1:5000/acceptString', {
      string: transcript,
      language: 'cpp'
    });

    console.log(response.data);

    if(response.data.code != null) {
      setCode(code + response.data.code);
    }

    else {
      console.log("got null");
    }

    resetTranscript();
  }

  return (

    <div className='h-screen w-screen'>

      <div className='m-5 w-fit rounded-md p-2 text-white bg-orange-600 text-lg'> Language pick </div>
      
      <div className='grid grid-cols-6 m-5 h-screen'>
        
        <textarea className='col-span-4 p-2 h-4/5 bg-blue-900 text-white' value={ code || " "}/>

        <div className='col-span-2'>

          <div className='flex justify-center'>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-green-600 text-white hover:bg-green-500' onClick={SpeechRecognition.startListening}> Listen </div>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-red-600 text-white hover:bg-red-500' onClick={SpeechRecognition.stopListening}> Stop </div>
          </div>

          <div className='m-5 p-2 h-1/6 w-10/12 bg-blue-200 text-black'> {transcript} </div>

          <div className='m-2 p-2 bg-blue-900 text-white w-fit mx-auto hover:bg-blue-800' onClick={() => sendString()}>
            accept
          </div>

          <div className='m-5 p-2 bg-orange-500 text-white w-fit'>
            Execute
          </div>

          <div className='m-5 p-2 bg-slate-500 text-white w-fit'>
            Output
          </div>

        </div>

      </div>

    </div>
    
  );
}

export default App;
