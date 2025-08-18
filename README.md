# LexiLeap

A lightweight typing-practice web app. Choose a level, hear each word pronounced, type it with per-character feedback, and track **time**, **accuracy**, and **WPM**.
Frontend is vanilla HTML/CSS/JS; backend is Flask + Postgres.

---

## Project Structure

```
LexiLeap/
├─ back2/                    # Flask + Postgres backend
│  ├─ lessens/               # lesson text files: lesson{N}.txt
│  ├─ DatabaseManager.py     # DB connection + update logic
│  ├─ lessons_fs.py          # loads and tokenizes lesson files
│  └─ server.py              # API routes + CORS
└─ front2/                   # static frontend
   ├─ screen1/
   │  ├─ screen1.html
   │  ├─ screen1.css
   │  └─ screen1.js
   ├─ screen2/
   │  ├─ screen2.html
   │  ├─ screen2.css
   │  └─ screen2.js
   ├─ api.js                 # tiny client for the API
   ├─ timer.js               # start/pause/stop timer
   └─ utility.js             # localStorage helpers
```

---

## What the Site Does

### Screen 1 — **Level Selection**

* Displays all lessons as tiles with:

  * **Score** (best score so far)
  * **Lock state** (locked/unlocked)
* Clicking a tile stores the chosen level index in `localStorage` (`levelNumber`) and navigates to Screen 2.
* Data source: `GET /get_levels` (returns `{ id, score, locked }` for each lesson).

### Screen 2 — **Typing Practice**

* Loads the selected lesson and renders a **character grid**:

  * Each typed character becomes **green** (correct) or **red** (incorrect).
  * The current cell is highlighted; the view auto-scrolls to keep it centered.
* **Speech Synthesis**: the current word is spoken; you can replay it anytime.
* **Timer**: visible clock; controls for start/pause/stop.
* **Live stats**:

  * **Accuracy**: per-word score (0–10) averaged and shown as a percentage.
  * **Speed**: WPM computed from total time and words evaluated.
* **Finish behavior**: when the last character is typed, the app **saves your score** and returns to Screen 1.

### Scoring & Unlock Logic

* Each word is compared **position-by-position** (case-insensitive).
  Per-word score: `ceil((correct_chars / word_length) * 10)` → 0..10.
* **Final accuracy** is the average of all word scores → 0–100%.
* On finish the backend:

  * Updates a lesson only if the new score is **higher** than the stored one.
  * If the new score is **≥ 60**, it **unlocks the next lesson**.

---

## How It Works (Under the Hood)

* **Lessons** live in `back2/lessens/lesson{N}.txt` and are split on whitespace into `words`, returned as `{ level, text, words }`.
* **Index vs. ID**:

  * The UI uses a **0-based** `levelNumber`.
  * The DB table `public.lessons` uses a **1-based** `id`.
  * Map accordingly when saving (e.g., `db_id = levelNumber + 1`).
* **Keyboard Input**:

  * Non-character keys are ignored.
  * For each character: mark correctness, advance caret, if a space was typed—score the word and speak the next one.
  * When the final index is reached, save is triggered immediately (no extra key needed).

---

## API

> Adjust HTTP methods to your server configuration (project supports either GET or POST for saving).

* `GET /get_levels` → `[{ id, score, locked }, ...]`
* `GET /get_level/<int:num>` → `{ level, text, words }` for the requested index
* `GET|POST /save_lesson/<int:id>/<int:score>` → saves the new best score and unlocks the next lesson if `score ≥ 60`

---

## Running Locally

### Backend (Flask)

```bash
cd back2
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
. .venv/bin/activate

pip install flask flask-cors psycopg2-binary
python server.py
```

* Server: `http://127.0.0.1:5000`
* Configure DB credentials in `DatabaseManager.py`.

### Frontend (Static)

```bash
cd front2
python -m http.server 5501
```

Open: `http://127.0.0.1:5501/screen1/screen1.html`
The backend has CORS enabled for local development so the frontend can call it from a different port.

---

## Tech Notes

* **Frontend**: vanilla HTML/CSS/JS, Web Speech API for pronunciation.
* **Backend**: Flask with CORS; Postgres for scores/locks.
* **Data model**: `public.lessons (id SERIAL, score INT, locked BOOLEAN)`.

---

## Roadmap (Nice-to-Have)

* Per-user profiles and score history
* Backspace/error-recovery modes
* Multi-voice selection and adjustable speech rate
* Environment-based configuration for DB and CORS
