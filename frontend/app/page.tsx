"use client";

import { useState } from "react";
import { fitConfig, type FitLevel } from "@/lib/fit-config";

interface Requirements {
  required_skills: string[];
  years_experience: number;
  tech_stack: string[];
}

interface FitReport {
  fit_level: FitLevel;
  fit_summary: string;
  strengths: string[];
  gaps: string[];
  talking_points: string[];
}

interface AnalysisResult {
  requirements: Requirements;
  fit_report: FitReport;
}

const API_URL = "/api/analyze";

export default function Home() {
  const [jobPosting, setJobPosting] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!jobPosting.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_posting: jobPosting }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Something went wrong.");
        return;
      }

      setResult(data);
    } catch {
      setError("Could not reach the API. Check your connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-space-bg text-gray-200 font-sans">
      {/* Header */}
      <header className="border-b border-space-border px-6 py-5">
        <div className="max-w-3xl mx-auto flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-violet-500 shadow-[0_0_8px_2px_rgba(139,92,246,0.6)]" />
          <span className="text-sm font-medium tracking-widest uppercase text-violet-400">
            Rubric
          </span>
          <span className="text-space-dim select-none">|</span>
          <span className="text-sm text-gray-500">Job-Fit Analyzer</span>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-14 flex flex-col gap-10">
        {/* Title */}
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight text-gray-100">
            Analyze a job posting
          </h1>
          <p className="text-gray-500 text-sm leading-relaxed">
            Paste a job description below. Rubric extracts requirements, matches
            them against your resume, and generates an honest fit report.
          </p>
        </div>

        {/* Input */}
        <div className="flex flex-col gap-3">
          <textarea
            value={jobPosting}
            onChange={(e) => setJobPosting(e.target.value)}
            placeholder="Paste job posting here..."
            rows={10}
            className="w-full rounded-xl border border-space-border bg-space-panel px-4 py-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-violet-600 focus:ring-1 focus:ring-violet-600 transition-colors"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !jobPosting.trim()}
            className="self-end px-6 py-2.5 rounded-lg bg-space-accent hover:bg-violet-600 disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium text-white transition-colors"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-900/50 bg-red-950/30 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        {result && (
          <div className="flex flex-col gap-8">
            {/* Fit Report — primary output */}
            {result.fit_report && (() => {
              const display = fitConfig[result.fit_report.fit_level];
              return (
                <section className="flex flex-col gap-4">
                  <h2 className="text-xs font-semibold tracking-widest uppercase text-violet-400">
                    Fit Report
                  </h2>
                  <div className={`rounded-xl border ${display.border} ${display.bg} p-5 flex flex-col gap-5`}>
                    <span className={`text-sm font-semibold ${display.color}`}>
                      {display.label}
                    </span>
                    <p className="text-sm text-gray-300 leading-relaxed">
                      {result.fit_report.fit_summary}
                    </p>
                    <div className="flex flex-col gap-2">
                      <span className="text-xs text-gray-500 uppercase tracking-widest">Strengths</span>
                      <ul className="flex flex-col gap-1.5">
                        {result.fit_report.strengths.map((s, i) => (
                          <li key={i} className="text-sm text-gray-300 flex gap-2">
                            <span className="text-emerald-500 mt-0.5">+</span>
                            {s}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="flex flex-col gap-2">
                      <span className="text-xs text-gray-500 uppercase tracking-widest">Gaps</span>
                      <ul className="flex flex-col gap-1.5">
                        {result.fit_report.gaps.map((g, i) => (
                          <li key={i} className="text-sm text-gray-300 flex gap-2">
                            <span className="text-red-500 mt-0.5">−</span>
                            {g}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="flex flex-col gap-2">
                      <span className="text-xs text-gray-500 uppercase tracking-widest">Talking Points</span>
                      <ul className="flex flex-col gap-1.5">
                        {result.fit_report.talking_points.map((t, i) => (
                          <li key={i} className="text-sm text-gray-300 flex gap-2">
                            <span className="text-violet-400 mt-0.5">→</span>
                            {t}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </section>
              );
            })()}

            {/* Extracted requirements — secondary */}
            <section className="flex flex-col gap-4">
              <h2 className="text-xs font-semibold tracking-widest uppercase text-violet-400">
                Extracted Requirements
              </h2>
              <div className="rounded-xl border border-space-border bg-space-panel p-5 flex flex-col gap-5">
                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0">Experience</span>
                  <span className="text-sm text-gray-200">
                    {result.requirements.years_experience} yr{result.requirements.years_experience !== 1 ? "s" : ""}
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0 pt-0.5">Required skills</span>
                  <div className="flex flex-wrap gap-2">
                    {result.requirements.required_skills.map((skill) => (
                      <span key={skill} className="px-2.5 py-0.5 rounded-full text-xs border border-violet-800/60 bg-violet-950/40 text-violet-300">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0 pt-0.5">Tech stack</span>
                  <div className="flex flex-wrap gap-2">
                    {result.requirements.tech_stack.map((tech) => (
                      <span key={tech} className="px-2.5 py-0.5 rounded-full text-xs border border-indigo-800/50 bg-indigo-950/30 text-indigo-300">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </section>

          </div>
        )}
      </main>
    </div>
  );
}
