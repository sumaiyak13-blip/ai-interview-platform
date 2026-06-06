import { useState } from "react";
import WelcomeScreen from "./components/WelcomeScreen";
import InterviewScreen from "./components/InterviewScreen";
import FeedbackScreen from "./components/FeedbackScreen";

function App() {
  // Application flow sequence states: 'welcome' -> 'interview' -> 'feedback'
  const [currentScreen, setCurrentScreen] = useState("welcome");

  return (
    <div className="min-h-screen bg-slate-900">
      {currentScreen === "welcome" && (
        <WelcomeScreen onStart={() => setCurrentScreen("interview")} />
      )}
      
      {currentScreen === "interview" && (
        <InterviewScreen onComplete={() => setCurrentScreen("feedback")} />
      )}
      
      {currentScreen === "feedback" && (
        <FeedbackScreen />
      )}
    </div>
  );
}

export default App;