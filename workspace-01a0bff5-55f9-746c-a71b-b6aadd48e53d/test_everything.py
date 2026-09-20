"""Full QA suite: every endpoint on BOTH backends + file deliverables."""
import io
import json
import os
import urllib.request

PASS, FAIL = 0, 0
FAILS = []


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✔ {name}" + (f"  ({extra})" if extra else ""))
    else:
        FAIL += 1
        FAILS.append(name)
        print(f"  ✘ {name}  {extra}")


def req(base, method, path, body=None, form=None):
    url = base + path
    data = None
    headers = {}
    if form is not None:
        data = form
        headers["Content-Type"] = "multipart/form-data; boundary=x"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def multipart_resume():
    body = (b"--x\r\nContent-Disposition: form-data; name=\"files\"; filename=\"t.txt\"\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Test Person\nSoftware Engineer\ntest@x.com\n\nSKILLS\nPython, SQL, Docker\n\n"
            b"EXPERIENCE\n3 years of experience building APIs.\n\nEDUCATION\nB.Tech CSE 2022\r\n--x--\r\n")
    return body


def test_backend(base, label):
    print(f"\n=== {label} @ {base} ===")

    # UI + static
    s, html = req(base, "GET", "/")
    check("GET / serves React UI", s == 200 and b"<div id=\"root\">" in html)
    js = html.split(b"src=\"")[1].split(b"\"")[0].decode() if b"src=\"" in html else None
    if js:
        s2, _ = req(base, "GET", js if js.startswith("/") else "/" + js)
        check("JS bundle loads", s2 == 200)

    # metadata
    s, b = req(base, "GET", "/api/health")
    h = json.loads(b)
    check("GET /api/health", s == 200 and h["status"] == "ok", h.get("backend", "?"))
    s, b = req(base, "GET", "/api/agents")
    check("GET /api/agents → 5 agents", s == 200 and len(json.loads(b)) == 5)

    # settings
    s, b = req(base, "POST", "/api/settings", {"gemini_key": "", "model": ""})
    check("POST /api/settings", s == 200 and json.loads(b)["llm_configured"] is False)

    # resume: paste
    s, b = req(base, "POST", "/api/resumes", {"text": "Test Person\nSoftware Engineer\nSKILLS\nPython, SQL, Docker\n3 years of experience\nB.Tech CSE", "filename": "t.txt"})
    added = json.loads(b).get("added", [])
    check("POST /api/resumes (paste) extracts profile", s == 200 and len(added) == 1
          and added[0]["profile"]["skills"], added[0]["profile"]["name"] if added else "none")
    rid = added[0]["id"] if added else None

    # resume: multipart upload
    s, b = req(base, "POST", "/api/resumes/upload", form=multipart_resume())
    up = json.loads(b).get("added", [])
    check("POST /api/resumes/upload (multipart)", s == 200 and len(up) == 1)
    if up:
        req(base, "DELETE", f"/api/resumes/{up[0]['id']}")

    s, b = req(base, "GET", "/api/resumes")
    check("GET /api/resumes lists", s == 200 and len(json.loads(b)["resumes"]) >= 1)

    # job: add
    s, b = req(base, "POST", "/api/jobs", {"text": "QA Tester\nRequirements (must have)\n- Python\n- SQL\n- 2+ years of experience\nNice to have\n- Docker", "filename": "qa.txt"})
    job = json.loads(b).get("job")
    check("POST /api/jobs extracts must/nice", s == 200 and job and
          any(x["name"] == "python" for x in job["requirements"]["must_have_skills"]) and
          any(x["name"] == "docker" for x in job["requirements"]["nice_to_have_skills"]))
    jid = job["id"] if job else None

    # match with 1 resume
    if jid:
        s, b = req(base, "POST", "/api/match", {"job_id": jid})
        m = json.loads(b)
        check("POST /api/match (small set)", s == 200 and len(m["ranked"]) >= 1 and
              "components" in m["ranked"][0] and "trace" in m["ranked"][0])
        req(base, "DELETE", f"/api/jobs/{jid}")

    # error paths
    s, b = req(base, "POST", "/api/match", {"job_id": "nope"})
    check("match unknown job → 404", s == 404)
    s, b = req(base, "DELETE", "/api/resumes/deadbeef")
    check("delete unknown resume → 404", s == 404)

    # demo load + full matching
    s, b = req(base, "POST", "/api/demo/load")
    d = json.loads(b)
    check("POST /api/demo/load → 10 resumes + 3 jobs", s == 200 and len(d["resumes"]) == 10 and len(d["jobs"]) == 3)

    expected_top = {"Senior Machine Learning Engineer": ("Aarav Sharma", 95.0),
                    "Full-Stack Web Developer": ("Sneha Kulkarni", 100.0),
                    "Data Analyst": ("Karan Patel", 80.7)}
    for job in d["jobs"]:
        s, b = req(base, "POST", "/api/match", {"job_id": job["id"]})
        m = json.loads(b)
        title = m["job"]["title"].split("—")[0].strip()
        exp_name, exp_score = expected_top[title]
        top = m["ranked"][0]
        scores = [r["total"] for r in m["ranked"]]
        check(f"match '{title}': 10 ranked, sorted desc", s == 200 and len(m["ranked"]) == 10 and scores == sorted(scores, reverse=True))
        check(f"match '{title}': #1 = {exp_name} @ {exp_score}", top["name"] == exp_name and abs(top["total"] - exp_score) < 0.01,
              f"got {top['name']} @ {top['total']}")
        check(f"match '{title}': explainability fields", all(k in top for k in ("components", "gaps", "summary", "trace")))

    # reextract (offline) + reset
    s, b = req(base, "POST", "/api/reextract")
    check("POST /api/reextract", s == 200 and json.loads(b)["resumes"] == 10)
    s, b = req(base, "DELETE", "/api/reset")
    check("DELETE /api/reset clears", s == 200)
    s, b = req(base, "GET", "/api/health")
    check("health after reset = 0/0", json.loads(b)["resumes"] == 0 and json.loads(b)["jobs"] == 0)


def test_files():
    print("\n=== Deliverable files ===")
    files = [
        "README.md",
        "test_pipeline.py", "test_everything.py",
        "backend/main.py", "backend/requirements.txt",
        "backend_django/manage.py", "backend_django/hiremind/views.py",
        "frontend/package.json", "frontend/src/App.jsx",
        "backend/static/index.html",
        "data/resumes/01_aarav_sharma_ml_engineer.txt", "data/jobs/jd1_senior_ml_engineer.txt",
        "docs/architecture.png",
        "docs/HireMind_AI_ProjectReport_PS03.pdf",
        "docs/HireMind_AI_Report_Simple.pdf",
        "docs/HireMind_AI_Report_Simple.docx",
        "docs/PS03_Documentation_HireMind_AI.docx",
        "docs/HireMind_AI_PitchDeck_PS03.pptx",
    ]
    for f in files:
        ok = os.path.exists("/home/user/" + f) and os.path.getsize("/home/user/" + f) > 0
        check(f"file {f}", ok)
    import glob
    check("10 demo resumes on disk", len(glob.glob("/home/user/data/resumes/*.txt")) == 10)
    check("3 demo jobs on disk", len(glob.glob("/home/user/data/jobs/*.txt")) == 3)
    check("7 kid diagrams on disk", len(glob.glob("/home/user/docs/shots/k*.png")) == 7)
    check("5 UI screenshots on disk", len(glob.glob("/home/user/docs/shots/0*.png")) == 5)


if __name__ == "__main__":
    test_backend("http://localhost:8000", "FastAPI backend")
    test_backend("http://localhost:8001", "Django backend")
    test_files()
    print(f"\n{'=' * 50}\nTOTAL: {PASS} passed, {FAIL} failed")
    if FAILS:
        print("FAILED:", *FAILS, sep="\n  - ")
        raise SystemExit(1)
    print("ALL CHECKS PASSED ✔")
