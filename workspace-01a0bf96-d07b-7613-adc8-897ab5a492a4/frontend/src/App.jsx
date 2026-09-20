import React, { useEffect, useState } from "react";
import { api } from "./api";
import Header from "./components/Header";
import PipelineBar from "./components/PipelineBar";
import ResumesTab from "./components/ResumesTab";
import JobsTab from "./components/JobsTab";
import ResultsTab from "./components/ResultsTab";

export default function App() {
  const [tab, setTab] = useState("resumes");
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [results, setResults] = useState({});
  const [activeJobId, setActiveJobId] = useState(null);
  const [busy, setBusy] = useState(null);
  const [running, setRunning] = useState(false);
  const [runningStep, setRunningStep] = useState(0);
  const [toast, setToast] = useState(null);
  const [agents, setAgents] = useState([]);
  const [llm, setLlm] = useState({ configured: false });

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 4500);
  };

  const refreshLlm = async () => {
    try {
      setLlm(await api.settingsGet());
    } catch {}
  };

  useEffect(() => {
    api.agents().then(setAgents).catch(() => {});
    refreshLlm();
    api.listResumes().then((d) => setResumes(d.resumes)).catch(() => {});
    api.listJobs().then((d) => setJobs(d.jobs)).catch(() => {});
  }, []);

  const loadDemo = async () => {
    setBusy("Loading demo dataset — Resume Agent & Job Agent extracting structure…");
    try {
      const d = await api.loadDemo();
      setResumes(d.resumes);
      setJobs(d.jobs);
      setResults({});
      setActiveJobId(d.jobs[0]?.id || null);
      showToast(`Loaded ${d.resumes.length} resumes & ${d.jobs.length} job descriptions`);
    } catch (e) {
      showToast("Demo load failed: " + e.message);
    }
    setBusy(null);
  };

  const addResumeFiles = async (files) => {
    setBusy(`Resume Agent extracting ${files.length} resume(s)…`);
    try {
      const d = await api.addResumeFiles(files);
      setResumes((r) => [...r, ...d.added]);
      showToast(`Added ${d.added.length} resume(s)`);
    } catch (e) {
      showToast(e.message);
    }
    setBusy(null);
  };

  const addResumeText = async (text, filename) => {
    setBusy("Resume Agent extracting profile…");
    try {
      const d = await api.addResumeText(text, filename);
      setResumes((r) => [...r, ...d.added]);
      showToast("Resume added");
    } catch (e) {
      showToast(e.message);
    }
    setBusy(null);
  };

  const delResume = async (id) => {
    try {
      await api.deleteResume(id);
      setResumes((r) => r.filter((x) => x.id !== id));
    } catch (e) {
      showToast(e.message);
    }
  };

  const addJob = async (text) => {
    setBusy("Job Agent parsing requirements…");
    try {
      const d = await api.addJob(text, text.split("\n")[0].slice(0, 60) + ".txt");
      setJobs((j) => [...j, d.job]);
      setActiveJobId(d.job.id);
      showToast("Job description added");
    } catch (e) {
      showToast(e.message);
    }
    setBusy(null);
  };

  const delJob = async (id) => {
    try {
      await api.deleteJob(id);
      setJobs((j) => j.filter((x) => x.id !== id));
      if (activeJobId === id) setActiveJobId(null);
    } catch (e) {
      showToast(e.message);
    }
  };

  const runMatch = async (jobId) => {
    setRunning(true);
    setRunningStep(1);
    setTab("results");
    const timer = setInterval(() => setRunningStep((s) => Math.min(s + 1, 5)), 700);
    try {
      const d = await api.match(jobId);
      clearInterval(timer);
      setRunningStep(5);
      setResults((r) => ({ ...r, [jobId]: d }));
      setActiveJobId(jobId);
      setTimeout(() => {
        setRunning(false);
        setRunningStep(0);
      }, 800);
    } catch (e) {
      clearInterval(timer);
      setRunning(false);
      setRunningStep(0);
      showToast("Matching failed: " + e.message);
    }
  };

  const saveSettings = async (key, model) => {
    await api.settingsSave(key, model);
    await refreshLlm();
  };

  const reextract = async () => {
    setBusy("Re-running Resume & Job Agent extraction with Gemini…");
    try {
      await api.reextract();
      const [r, j] = await Promise.all([api.listResumes(), api.listJobs()]);
      setResumes(r.resumes);
      setJobs(j.jobs);
      setResults({});
      showToast("Re-extraction complete — results cleared, run matching again");
    } catch (e) {
      showToast(e.message);
    }
    setBusy(null);
  };

  const resetAll = async () => {
    try {
      await api.reset();
      setResumes([]);
      setJobs([]);
      setResults({});
      setActiveJobId(null);
      showToast("All data cleared");
    } catch (e) {
      showToast(e.message);
    }
  };

  return (
    <div className="app">
      <Header llm={llm} onSaveSettings={saveSettings} onReextract={reextract} onReset={resetAll} />
      <PipelineBar agents={agents} runningStep={runningStep} />

      {busy && (
        <div className="busybar">
          <span className="spinner" />
          {busy}
        </div>
      )}
      {toast && <div className="toast">{toast}</div>}

      <nav className="tabs">
        <button className={tab === "resumes" ? "active" : ""} onClick={() => setTab("resumes")}>
          1 · Resumes <span className="count">{resumes.length}</span>
        </button>
        <button className={tab === "jobs" ? "active" : ""} onClick={() => setTab("jobs")}>
          2 · Job Descriptions <span className="count">{jobs.length}</span>
        </button>
        <button className={tab === "results" ? "active" : ""} onClick={() => setTab("results")}>
          3 · Ranked Matches
        </button>
      </nav>

      {tab === "resumes" && (
        <ResumesTab resumes={resumes} onUpload={addResumeFiles} onPaste={addResumeText} onDemo={loadDemo} onDelete={delResume} busy={busy} />
      )}
      {tab === "jobs" && <JobsTab jobs={jobs} onAdd={addJob} onDemo={loadDemo} onDelete={delJob} busy={busy} />}
      {tab === "results" && (
        <ResultsTab
          jobs={jobs}
          resumes={resumes}
          results={results}
          activeJobId={activeJobId}
          setActiveJobId={setActiveJobId}
          onRun={runMatch}
          running={running}
          runningStep={runningStep}
        />
      )}

      <footer>
        HireMind AI · PS03 Multi-Agent Resume Screening &amp; Job Matching · React + FastAPI + Gemini · Matching Agent is deterministic for full explainability · Demo data is synthetic
      </footer>
    </div>
  );
}
