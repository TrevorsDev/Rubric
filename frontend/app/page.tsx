"use client";

import { useState } from "react";

interface Requirements {
  required_skills: string[];
  years_experience: number;
  tech_stack: string[];
}

interface ResumeChunk {
  type: string;
  title: string;
  content: string;
  skills: string[];
}

interface AnalysisResult {
  requirements: Requirements;
  matching_chunks: ResumeChunk[];
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
    <div className="min-h-screen bg-[#09090f] text-gray-200 font-sans">
      {/* Header */}
      <header className="border-b border-[#1e1a35] px-6 py-5">
        <div className="max-w-3xl mx-auto flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-violet-500 shadow-[0_0_8px_2px_rgba(139,92,246,0.6)]" />
          <span className="text-sm font-medium tracking-widest uppercase text-violet-400">
            Rubric
          </span>
          <span className="text-[#2a2450] select-none">|</span>
          <span className="text-sm text-gray-500">Job-Fit Analyzer</span>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-14 flex flex-col gap-10">
        {/* Title block */}
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight text-gray-100">
            Analyze a job posting
          </h1>
          <p className="text-gray-500 text-sm leading-relaxed">
            Paste a job description below. The analyzer extracts the required
            skills and surfaces the most relevant sections of my resume.
          </p>
        </div>

        {/* Input */}
        <div className="flex flex-col gap-3">
          <textarea
            value={jobPosting}
            onChange={(e) => setJobPosting(e.target.value)}
            placeholder="Paste job posting here..."
            rows={10}
            className="w-full rounded-xl border border-[#1e1a35] bg-[#0e0d1a] px-4 py-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-violet-600 focus:ring-1 focus:ring-violet-600 transition-colors"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !jobPosting.trim()}
            className="self-end px-6 py-2.5 rounded-lg bg-violet-700 hover:bg-violet-600 disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium text-white transition-colors"
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

        {/* Results */}
        {result && (
          <div className="flex flex-col gap-8">
            {/* Extracted requirements */}
            <section className="flex flex-col gap-4">
              <h2 className="text-xs font-semibold tracking-widest uppercase text-violet-400">
                Extracted Requirements
              </h2>

              <div className="rounded-xl border border-[#1e1a35] bg-[#0e0d1a] p-5 flex flex-col gap-5">
                {/* Years experience */}
                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0">
                    Experience
                  </span>
                  <span className="text-sm text-gray-200">
                    {result.requirements.years_experience} yr
                    {result.requirements.years_experience !== 1 ? "s" : ""}
                  </span>
                </div>

                {/* Required skills */}
                <div className="flex items-start gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0 pt-0.5">
                    Required skills
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {result.requirements.required_skills.map((skill) => (
                      <span
                        key={skill}
                        className="px-2.5 py-0.5 rounded-full text-xs border border-violet-800/60 bg-violet-950/40 text-violet-300"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Tech stack */}
                <div className="flex items-start gap-3">
                  <span className="text-xs text-gray-500 w-32 shrink-0 pt-0.5">
                    Tech stack
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {result.requirements.tech_stack.map((tech) => (
                      <span
                        key={tech}
                        className="px-2.5 py-0.5 rounded-full text-xs border border-indigo-800/50 bg-indigo-950/30 text-indigo-300"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </section>

            {/* Matching resume chunks */}
            <section className="flex flex-col gap-4">
              <h2 className="text-xs font-semibold tracking-widest uppercase text-violet-400">
                Matching Resume Sections
              </h2>

              {result.matching_chunks.length === 0 ? (
                <p className="text-sm text-gray-500">
                  No matching sections found.
                </p>
              ) : (
                <div className="flex flex-col gap-3">
                  {result.matching_chunks.map((chunk, i) => (
                    <div
                      key={i}
                      className="rounded-xl border border-[#1e1a35] bg-[#0e0d1a] p-5 flex flex-col gap-3"
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-gray-100">
                          {chunk.title}
                        </span>
                        <span className="text-xs px-2 py-0.5 rounded-full border border-[#2a2450] text-gray-500">
                          {chunk.type}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400 leading-relaxed">
                        {chunk.content}
                      </p>
                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {chunk.skills.map((skill) => (
                          <span
                            key={skill}
                            className="text-xs text-gray-600 border border-[#1e1a35] rounded px-1.5 py-0.5"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}
