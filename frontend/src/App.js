import logo from './logo.svg';
import './App.css';
import React, { Component, useState } from 'react';
import SpeechRecognition, {useSpeechRecognition} from 'react-speech-recognition';

function App() {

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Brower doesnt support speech</span>;
  }

  return (
    <div className='h-screen w-screen'>
      <div className='m-5 w-fit rounded-md p-2 text-white bg-orange-600 text-lg'> Language pick </div>
      
      <div className='flex m-5 h-screen'>
        
        <textarea className=' p-2 h-4/5 w-4/6 bg-blue-900 text-white'>hello</textarea>

        <div className='grow'>

          <div className='flex justify-center'>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-green-600 text-white hover:bg-green-500' onClick={SpeechRecognition.startListening}> Listen </div>
            <div className='ml-5 w-100 h-fit p-5 rounded-full bg-red-600 text-white hover:bg-red-500' onClick={SpeechRecognition.stopListening}> Stop </div>
          </div>

          <div className='m-5 p-2 h-1/6 w-10/12 bg-blue-200 text-black'> {transcript} </div>

          <div className='m-2 p-2 bg-blue-900 text-white w-fit mx-auto' onClick={resetTranscript}>
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
    </div >
  );
}

export default App;
