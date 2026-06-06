export default function WelcomeScreen({ onStart }) {
  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center p-6">
      <div className="max-w-3xl w-full text-center space-y-8 bg-slate-800/40 p-10 rounded-3xl border border-slate-700/50 backdrop-blur-sm shadow-2xl">
        
        {/* Decorative Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
          🚀 Next-Gen Interview Prep
        </div>

        {/* Main Heading */}
        <div className="space-y-3">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-slate-100 via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
            AI-Powered Mock Simulator
          </h1>
          <p className="text-slate-400 max-w-xl mx-auto text-base md:text-lg leading-relaxed">
            Practice technical and ML core questions in a real-time environment. Get analyzed instantly on parameters that matter.
          </p>
        </div>

        {/* Features Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 text-left">
          <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/40">
            <div className="text-indigo-400 text-xl mb-2">📹</div>
            <h3 className="font-semibold text-slate-200 text-sm mb-1">Live Capture</h3>
            <p className="text-xs text-slate-400">Records your speech response seamlessly per question.</p>
          </div>
          <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/40">
            <div className="text-indigo-400 text-xl mb-2">⏱️</div>
            <h3 className="font-semibold text-slate-200 text-sm mb-1">Smart Timer</h3>
            <p className="text-xs text-slate-400">60-second pressure window mimicking real screening conditions.</p>
          </div>
          <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/40">
            <div className="text-indigo-400 text-xl mb-2">📊</div>
            <h3 className="font-semibold text-slate-200 text-sm mb-1">Radar Insights</h3>
            <p className="text-xs text-slate-400">Instant metrics delivery on your programming vocabulary.</p>
          </div>
        </div>

        {/* Call to Action Button */}
        <div className="pt-4">
          <button
            onClick={onStart}
            className="group relative inline-flex items-center justify-center bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3.5 px-8 rounded-2xl transition duration-200 shadow-xl shadow-indigo-600/20 hover:shadow-indigo-600/30 active:scale-[0.98] overflow-hidden"
          >
            <span>Start AI Assessment</span>
            <span className="ml-2 transform group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>

      </div>
    </div>
  );
}