"""Capture UI screenshots of the running HireMind AI app for the PDF report."""
import time
from playwright.sync_api import sync_playwright

OUT = "/home/user/docs/shots/"
import os
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8000", wait_until="networkidle")
    page.wait_for_selector(".card", timeout=15000)   # resume cards visible (data preloaded)
    time.sleep(0.5)
    page.screenshot(path=OUT + "01_resumes.png")
    print("shot 1: resumes tab")

    page.click("nav.tabs button:nth-child(2)")      # Jobs tab
    page.wait_for_selector(".grid .card", timeout=10000)
    time.sleep(0.4)
    page.screenshot(path=OUT + "02_jobs.png")
    print("shot 2: jobs tab")

    page.click("nav.tabs button:nth-child(3)")      # Results tab
    page.wait_for_selector(".jobpick .pill", timeout=10000)
    page.click(".jobpick .pill")                    # select first job
    page.wait_for_selector("button.run", timeout=10000)
    page.click("button.run")
    page.wait_for_selector(".rankrow", timeout=30000)
    time.sleep(1.0)
    page.screenshot(path=OUT + "03_ranked.png")
    print("shot 3: ranked matches")

    page.click(".rankrow")                          # open top candidate detail
    page.wait_for_selector(".detail", timeout=10000)
    time.sleep(0.5)
    page.screenshot(path=OUT + "04_detail.png")
    print("shot 4: explainable detail")

    # scroll detail to gaps section for a 5th shot
    page.eval_on_selector(".detail", "el => el.scrollTop = 700")
    time.sleep(0.4)
    page.screenshot(path=OUT + "05_detail_gaps.png")
    print("shot 5: detail gaps")

    browser.close()
print("screenshots done")
