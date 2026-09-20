"""End-to-end smoke test: load demo data, run matching for every job, print rankings.
Usage: python3 test_pipeline.py [base_url]   (default http://localhost:8000)"""
import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"


def post(path, body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else b"",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return json.loads(urllib.request.urlopen(req).read())


demo = post("/api/demo/load")
print(f"Loaded: {len(demo['resumes'])} resumes, {len(demo['jobs'])} jobs\n")

for job in demo["jobs"]:
    res = post("/api/match", {"job_id": job["id"]})
    print(f"=== {res['job']['title']} ===")
    for e in res["ranked"]:
        cov = e["components"]["must_have"]
        gaps = ", ".join(e["must_missing"][:3])
        line = f"  #{e['rank']:>2}  {e['total']:>5}  {e['verdict']:<14} {e['name']:<18} must {cov['matched']}/{cov['total']}"
        if gaps:
            line += f"   gaps: {gaps}"
        print(line)
    top = res["ranked"][0]
    print(f"  -> Recruiter summary (#1): {top['summary'][:200]}")
    print(f"  -> Gap analysis (#1): {top['gaps']['summary']}")
    print()

print("PIPELINE OK")
