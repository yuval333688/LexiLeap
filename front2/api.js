const api = (function () {
  // Generic GET JSON (works for Flask too)
  async function load(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json(); // return raw JSON (not data.record)
  }

  // Return the whole lesson object:
  // { level, text, words: [...] }
  async function load_lesson(num) {
    const url = `http://127.0.0.1:5000/get_level/${num}`;
    const data = await load(url);
    console.log("lesson:", data);
    return data; 
  }

  async function load_levelsScore() {
    const url = "http://127.0.0.1:5000/get_levels";
    const data = await load(url);
    // supports: array OR { levels: [...] }
    return Array.isArray(data) ? data : (data?.levels ?? []);
  }

  async function save_lesson(lesson_number, score) {
    console.log(score);
  const url = `http://127.0.0.1:5000/save_lesson/${lesson_number}/${score}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}


  return {
    load_lesson,
    save_lesson,
    load_levelsScore,
  };
})();
