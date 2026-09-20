const LS_KEY = "hm_gemini_key";
const LS_MODEL = "hm_gemini_model";

export function getKey() {
  return localStorage.getItem(LS_KEY) || "";
}
export function getModel() {
  return localStorage.getItem(LS_MODEL) || "";
}
export function saveKeyModel(key, model) {
  if (key) localStorage.setItem(LS_KEY, key);
  else localStorage.removeItem(LS_KEY);
  if (model) localStorage.setItem(LS_MODEL, model);
  else localStorage.removeItem(LS_MODEL);
}

function headers(json = true) {
  const h = {};
  if (getKey()) h["X-Gemini-Key"] = getKey();
  if (getModel()) h["X-Gemini-Model"] = getModel();
  if (json) h["Content-Type"] = "application/json";
  return h;
}

async function req(method, path, body, isForm = false) {
  const res = await fetch(path, {
    method,
    headers: headers(!isForm && body !== undefined),
    body: isForm ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      detail = j.detail || detail;
    } catch {}
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.json();
}

export const api = {
  agents: () => req("GET", "/api/agents"),
  settingsGet: () => req("GET", "/api/settings"),
  settingsSave: (gemini_key, model) => req("POST", "/api/settings", { gemini_key, model }),
  listResumes: () => req("GET", "/api/resumes"),
  listJobs: () => req("GET", "/api/jobs"),
  addResumeFiles: (files) => {
    const fd = new FormData();
    for (const f of files) fd.append("files", f);
    return req("POST", "/api/resumes/upload", fd, true);
  },
  addResumeText: (text, filename) => req("POST", "/api/resumes", { text, filename }),
  deleteResume: (id) => req("DELETE", `/api/resumes/${id}`),
  addJob: (text, filename) => req("POST", "/api/jobs", { text, filename }),
  deleteJob: (id) => req("DELETE", `/api/jobs/${id}`),
  match: (job_id) => req("POST", "/api/match", { job_id }),
  loadDemo: () => req("POST", "/api/demo/load"),
  reset: () => req("DELETE", "/api/reset"),
  reextract: () => req("POST", "/api/reextract"),
};
