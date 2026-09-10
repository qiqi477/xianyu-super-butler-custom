## Xianyu Super Butler - Custom (Progress)

This repo is a customized, incremental implementation focused on multi-account management and streamlined product publishing for local testing and quick iteration.

What's new in UI update (stage 1)
- Frontend redesigned to a compact dashboard layout resembling the provided screenshot: left compact nav, main publish form, right sidebar with accounts, material library and publish records.
- Image upload preview and validation (1-9 images).
- Save-as-material: save current form as a reusable material and import it later.
- Attribute recognition (keyword-based placeholder) that fills category/spec suggestions.

How to run locally (recommended)
1. Clone and switch to the working branch:
   git clone https://github.com/qiqi477/xianyu-super-butler-custom.git
   cd xianyu-super-butler-custom
   git checkout work/xianyu-custom

2. Create and activate virtualenv, install dependencies:
   python -m venv .venv
   source .venv/bin/activate   # Windows: .\\.venv\\Scripts\\activate
   pip install -r requirements.txt

3. Seed demo data (optional but helpful):
   python app/seed.py

4. Start the app:
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

5. Open the admin UI:
   http://localhost:8080/frontend/index.html

Docker (optional)
1. Copy .env.example to .env and edit as needed.
2. ./start.sh

Notes & next steps
- Current publish flow is simulated and records publishing in the local DB. To integrate with real platform publishing we need API docs or test credentials.
- Attribute recognition is a rule-based placeholder. I can integrate OpenAI or image-recognition later (you can add OPENAI_API_KEY to environment variables or GitHub Secrets).
- I will proceed to polish UI and add CSV batch import and admin auth next, unless you give other priorities.
