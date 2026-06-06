import { useEffect, useRef, useState } from "react";

export default function InterviewScreen({ onComplete }) {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  
  // Hardcoded technical/AI questions until Member 4's Gemini integration is ready
  const [questions] = useState([
    "Tell me about a challenging Python or AI/ML project you built.",
    "How do you optimize a slow database query or machine learning pipeline?",
    "Explain the fundamental difference between supervised and unsupervised learning."
  ]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);
  const [isRecording, setIsRecording] = useState(false);

  // 1. Initial Access: Start Webcam & Microphone on Page Load
  useEffect(() => {
    async function startStream() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        
        // Setup MediaRecorder using only the audio track for data efficiency
        const audioTrack = stream.getAudioTracks()[0];
        const audioStream = new MediaStream([audioTrack]);
        mediaRecorderRef.current = new MediaRecorder(audioStream);

        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorderRef.current.onstop = () => {
          // Creates a file out of the recorded audio chunks
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
          audioChunksRef.current = []; // Clear array for the next question
          
          console.log("--- PYTHON PIPELINE DATA READY ---");
          console.log("Audio file generated successfully:", audioBlob);
          // Member 1 will append this blob to a FormData object to pass to FastAPI
        };

        // Automatically start recording the first question
        startRecording();

      } catch (err) {
        console.error("Camera access denied or device disconnected:", err);
      }
    }
    startStream();

    // Clean up streams when user leaves the page
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // 2. Audio Recorder Controls
  const startRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "inactive") {
      mediaRecorderRef.current.start();
      setIsRecording(true);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // 3. 60-Second Countdown Clock Logic
  useEffect(() => {
    if (timeLeft === 0) {
      handleNextQuestion();
      return;
    }
    const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft]);

  // 4. State Transitions
  const handleNextQuestion = () => {
    stopRecording(); // Saving the audio stream for the current question

    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
      setTimeLeft(60); // Reset timer back to 60 seconds
      // Short delay to allow the hardware recorder state to clear
      setTimeout(() => startRecording(), 500);
    } else {
      alert("Interview Complete! Your answers have been successfully buffered for AI scoring.");
      onComplete();
    }
  };

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-slate-900 text-white p-6 gap-6 items-center justify-center">
      <div className="max-w-6xl w-full flex flex-col md:flex-row gap-6">
        
        {/* LEFT COMPONENT: Webcam Stream Interface */}
        <div className="flex-1 flex flex-col gap-4 w-full">
          <div className="relative rounded-2xl overflow-hidden bg-black aspect-video border border-slate-700 shadow-2xl">
            <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
            {isRecording && (
              <div className="absolute top-4 left-4 bg-red-600 px-3 py-1 rounded-full text-xs font-bold animate-pulse flex items-center gap-1.5 shadow-md">
                <span className="h-2 w-2 rounded-full bg-white"></span> LIVE RECORDING
              </div>
            )}
          </div>
          
          {/* Status Context Bar */}
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 flex items-center justify-between">
            <span className="text-sm text-slate-400 font-medium">Data Pipeline:</span>
            <span className={`text-xs px-2.5 py-1 rounded font-mono font-semibold ${isRecording ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-slate-700 text-slate-400'}`}>
              {isRecording ? "Capturing raw audio channels for Python processing..." : "Pipeline Idle"}
            </span>
          </div>
        </div>

        {/* RIGHT COMPONENT: Interactive Question Canvas */}
        <div className="w-full md:w-[400px] h-[400px] flex flex-col justify-between bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
          <div>
            <div className="flex justify-between items-center mb-6">
              <span className="text-xs font-bold tracking-wider text-indigo-400 uppercase bg-indigo-500/10 px-2.5 py-1 rounded-md">
                Question {currentIdx + 1} of {questions.length}
              </span>
              <div className={`px-3 py-1 rounded-full font-mono text-sm font-bold border ${timeLeft < 15 ? 'bg-red-500/10 text-red-400 border-red-500/30 animate-pulse' : 'bg-slate-700 text-slate-300 border-slate-600'}`}>
                00:{timeLeft < 10 ? `0${timeLeft}` : timeLeft}
              </div>
            </div>
            
            <h2 className="text-lg font-medium leading-relaxed text-slate-100">
              {questions[currentIdx]}
            </h2>
          </div>

          <button 
            onClick={handleNextQuestion}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-4 rounded-xl transition duration-200 mt-6 shadow-lg shadow-indigo-600/30 active:scale-[0.98]"
          >
            {currentIdx === questions.length - 1 ? "Complete Interview" : "Next Question →"}
          </button>
        </div>

      </div>
    </div>
  );
}