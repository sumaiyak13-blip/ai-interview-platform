import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";

// Mock AI evaluation metrics from the Python AIML backend
const performanceData = [
  { metric: "Technical Accuracy", score: 85 },
  { metric: "Communication", score: 72 },
  { metric: "Confidence", score: 88 },
  { metric: "STAR Structure", score: 60 },
  { metric: "Pacing", score: 80 },
];

export default function FeedbackScreen() {
  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 flex justify-center">
      <div className="max-w-5xl w-full space-y-8">
        
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-100">AI Interview Feedback</h1>
          <p className="text-slate-400 mt-1">Algorithmic analysis of your speech, body language, and Python/ML concepts.</p>
        </div>

        {/* Top Grid: Overall Score & Analytics Chart */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: Score Circle */}
          <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 flex flex-col items-center justify-center text-center shadow-lg">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">Overall Match Score</span>
            <div className="text-6xl font-extrabold text-indigo-400">77%</div>
            <div className="mt-4 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs px-3 py-1 rounded-full font-medium">
              Passed AI Screening
            </div>
          </div>

          {/* Card 2 & 3: Radar Chart Breakdown */}
          <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 md:col-span-2 h-72 shadow-lg flex flex-col justify-between">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">Evaluation Matrix</span>
            <ResponsiveContainer width="100%" height="90%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={performanceData}>
                <PolarGrid stroke="#475569" />
                <PolarAngleAxis dataKey="metric" stroke="#94a3b8" fontSize={11} />
                <Radar name="Your Metrics" dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bottom Section: AI Insights & Constructive Critiques */}
        <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-lg">
          <h3 className="text-lg font-bold text-slate-200 mb-4 flex items-center gap-2">
            🤖 Detailed AI Evaluation Notes
          </h3>
          <div className="space-y-4">
            <div className="flex gap-3 items-start border-b border-slate-700/50 pb-4">
              <span className="text-emerald-400 text-lg">✓</span>
              <div>
                <strong className="text-emerald-400 block mb-0.5">Strong Core Engineering Knowledge</strong>
                <p className="text-sm text-slate-300">You clearly explained the distinction between supervised algorithms and unsupervised grouping models with high technical accuracy.</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-amber-400 text-lg">⚠</span>
              <div>
                <strong className="text-amber-400 block mb-0.5">Improve Response Structure (STAR Method)</strong>
                <p className="text-sm text-slate-300">Your description of your past project lacked a specific, quantifiable metric. Try to explicitly describe the final "Result" (e.g., accuracy percentage or latency drop).</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}