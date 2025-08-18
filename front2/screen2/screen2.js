// screen2.js
{
  "use strict";

  /* ============================= DOM & STATE ============================== */
  let start_exercise_button;
  let sentence_display;
  let replay_word_button;
  let stop_button;
  let pause_button;
  let start_button;
  let time_div;
  let accuracy_div;
  let speed_div;

  // Speech synthesis
  let ready_to_speak = false;
  let speechSynthesisUtterance;

  // Lesson / typing state
  let levelNumber;
  let gamePlay = false;
  let words = [];            // lesson words
  let userWord = "";         // buffer for the typed word (resets on space)
  let sentenceChars = [];    // all characters + spaces
  let charSpans = [];        // span refs for each character
  let currentWordIndex = 0;  // index into `words`
  let currentCharIndex = 0;  // index into `sentenceChars`

  // Aggregated scoring for accuracy and speed
  let wordsEvaluated = 0;
  let totalScoreSum  = 0;    // sum of per-word scores (0..10 each)

  /* =============================== HELPERS ================================ */

  /** Highlight the container of the next character in blue. */
  function setNextCharHighlight(idx) {
    // Remove any previous highlight
    document.querySelectorAll(".char-container.next-char")
      .forEach(el => el.classList.remove("next-char"));

    // Add highlight to the next character's container if exists
    if (idx >= 0 && idx < charSpans.length) {
      charSpans[idx].parentElement.classList.add("next-char");
    }
  }

  /** Smoothly scroll so the current character is visible. */
  function focusChar() {
    if (currentCharIndex < 0 || currentCharIndex >= charSpans.length) return;
    charSpans[currentCharIndex].scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  /** Returns the current accuracy percentage (0–100). */
  function getAccuracy() {
    if (wordsEvaluated === 0) return 0;
    const avgScore0to10 = totalScoreSum / wordsEvaluated; // 0..10
    return Math.round(avgScore0to10 * 10);                 // -> 0..100
  }

  /** Returns current words-per-minute based on Timer.getSec() and wordsEvaluated. */
  function getWPM() {
    const sec = Timer.getSec();
    const minutes = sec > 0 ? (sec / 60) : 0;
    return minutes > 0 ? Math.round(wordsEvaluated / minutes) : 0;
  }

  /**
   * Returns an integer score 0..10 (ceil), comparing by position, case-insensitive.
   * Example: origin="cat", user="cet"  ->  2/3*10 = 6.66.. -> 7
   */
  function getAccuracyFor(origin, user) {
    console.log(origin + " , " + user);
    const a = String(origin || "");
    const b = String(user || "");
    if (a.length === 0) return 0;

    let correct = 0;
    for (let i = 0; i < a.length; i++) {
      if (b[i] && a[i].toLowerCase() === b[i].toLowerCase()) {
        correct++;
      }
    }
    const score0to10 = (correct / a.length) * 10;  // 0..10
    return Math.ceil(score0to10);                  // ceil like the old api.get_score
  }

  /* ============================= SCORING / UI ============================ */
  /**
   * Update running averages and UI after receiving a score for the last word.
   * origin: the original word from the lesson
   * user:   the user's typed word (until the space)
   *
   * Uses:
   *   getAccuracyFor(origin, user) -> integer in range 0..10 (ceil)
   *   Timer.getSec()               -> total seconds elapsed
   */
  function updataScore(origin, user) {
    // Compute score locally (synchronous)
    let score = Number(getAccuracyFor(origin, user));
    if (Number.isNaN(score)) score = 0;
    if (score < 0) score = 0;
    if (score > 10) score = 10;

    // Accumulate
    wordsEvaluated += 1;
    totalScoreSum  += score;

    // Update UI using helpers
    const accuracyPct = getAccuracy();
    const wpm         = getWPM();

    accuracy_div.textContent = `${accuracyPct}%`;
    speed_div.textContent    = `${wpm} w/m`;
  }

  /* ============================ INPUT HANDLING ============================ */
  /**
   * Handle key presses: mark correctness, advance caret, update highlight,
   * and when a space is typed — score the word and speak the next one.
   */
  function inputHandler(event) {
  // Ignore input when game is not active
  if (!gamePlay) return;

  const typedChar = event.key;

  // Guard if we somehow get extra keypress after finish
  if (currentCharIndex >= sentenceChars.length) {
    api.save_lesson(levelNumber,getAccuracy()).finally(stop);
    return;
  }

  const expected = sentenceChars[currentCharIndex];
  const span = charSpans[currentCharIndex];

  // Leave current cell: remove "next" highlight and any old hint
  span.classList.remove("next-char");
  const oldHint = span.parentElement.querySelector(".correct-hint");
  if (oldHint) oldHint.remove();

  // Mark correctness; if wrong (and not a space) show the expected char as a hint
  if (typedChar.toLowerCase() === expected.toLowerCase()) {
    span.classList.add("correct");
  } else {
    span.classList.add("incorrect");
    if (expected !== " ") {
      const hint = document.createElement("span");
      hint.className = "correct-hint";
      hint.textContent = expected;
      span.parentElement.appendChild(hint);
    }
  }

  // Render the typed character
  span.textContent = typedChar;

  // Accumulate user's word (skip spaces)
  if (typedChar !== " ") userWord += typedChar.toLowerCase();

  // Move to next character
  currentCharIndex++;

  // If a space was just typed, we finished a word: score and advance word index
  const justTypedSpace = sentenceChars[currentCharIndex - 1] === " ";
  if (justTypedSpace) {
    updataScore(words[currentWordIndex], userWord);
    userWord = "";
    currentWordIndex++;
  }

  

  // Keep caret visible and highlight the next character
  setNextCharHighlight(currentCharIndex);
  focusChar();

  // If we completed a word (and not finished), speak the next one
  if (justTypedSpace) replayWord();
}

  /* ========================== SCREEN LIFECYCLE =========================== */
  function main() {
    find_views();
    init_views();
  }

  /** Cache all DOM refs. */
  function find_views() {
    sentence_display       = document.getElementById("id_display_sentence");
    start_exercise_button  = document.getElementById("id_start_exercise_button");
    replay_word_button     = document.getElementById("id_replay_word_button");
    stop_button            = document.getElementById("id_stop_button");
    pause_button           = document.getElementById("id_pause_button");
    start_button           = document.getElementById("id_start_button");
    time_div               = document.getElementById("id_time");
    accuracy_div           = document.getElementById("id_accuracy");
    speed_div              = document.getElementById("id_speed");
  }

  /** Initialize timer, load lesson, build UI, and attach listeners. */
  function init_views() {

    init_speech();

    // Hook timer tick to time label
    Timer.init((tStr) => {
      time_div.textContent = tStr;
    });
    levelNumber = utility.loadNumber("levelNumber");
    console.log(levelNumber);

    // Load lesson words, build character grid, and start listening to typing
    api.load_lesson(levelNumber)
      .then(l_words => {
        console.log(l_words);
        init_words(l_words);
      })
      .then(() => {
        focusChar();
        document.addEventListener("keydown", inputHandler);
      });
  }

  /* ============================ SESSION CONTROLS ========================= */
  function start_exercise() {
    start_exercise_button.style.display = "none";
    replay_word_button.style.display    = "inline-block";
    stop_button.style.display           = "inline-block";
    pause_button.style.display          = "inline-block";
    start_button.style.display          = "none";
    gamePlay = true;
    replayWord();
    Timer.start();
  }

  function stop() {
    start_exercise_button.style.display = "none";
    replay_word_button.style.display    = "none";
    stop_button.style.display           = "none";
    pause_button.style.display          = "none";
    start_button.style.display          = "none";
    gamePlay = false;
    Timer.stop();
    window.location.href = "../screen1/screen1.html";
    
  }

  function pause() {
    start_exercise_button.style.display = "none";
    replay_word_button.style.display    = "none";
    stop_button.style.display           = "inline-block";
    pause_button.style.display          = "none";
    start_button.style.display          = "inline-block";
    gamePlay = false;
    Timer.pause();
  }

  function start() {
    start_exercise_button.style.display = "none";
    replay_word_button.style.display    = "inline-block";
    stop_button.style.display           = "inline-block";
    pause_button.style.display          = "inline-block";
    start_button.style.display          = "none";
    gamePlay = true;
    Timer.start();
  }

  /** Speak the current word again. */
  function replayWord() {
    speak(words[currentWordIndex]);
  }

  // // Expose controls for onclick handlers in HTML
  // window.start_exercise = start_exercise;
  // window.stop = stop;
  // window.pause = pause;
  // window.start = start;
  // window.replayWord = replayWord;

  /* ========================= BUILD SENTENCE DISPLAY ====================== */
  /** Build the visual cells for all characters (letters + spaces). */
  function init_words(l_words) {
    
    words = l_words.words;
    console.log(words);

    // Reset grids
    sentenceChars = [];
    charSpans = [];
    sentence_display.innerHTML = "";

    // Flatten words -> characters + trailing space after each word
    for (const word of words) {
      for (const c of word) sentenceChars.push(c);
      sentenceChars.push(" ");
    }

    // Create a cell (container + span) for each character
    for (const c of sentenceChars) {
      const charContainer = document.createElement("div");
      charContainer.classList.add("char-container");
      if (c === " ") charContainer.classList.add("space");

      const charSpan = document.createElement("span");
      charSpan.classList.add("typed-char");
      charSpan.textContent = ""; // initially empty until typed

      charContainer.appendChild(charSpan);
      sentence_display.appendChild(charContainer);
      charSpans.push(charSpan);
    }

    // Show blue highlight on the first char
    setNextCharHighlight(0);
  }

  /* =========================== SPEECH SYNTHESIS ========================== */
  /** Prepare voices and a reusable utterance. */
  function init_speech() {
    function setVoices() {
      const voices = window.speechSynthesis.getVoices();
      if (!voices || voices.length === 0) return;

      speechSynthesisUtterance = new SpeechSynthesisUtterance();
      console.log("Available voices:", voices);

      // Prefer en-US; otherwise first available
      const preferredVoice =
        voices.find(v => v.lang === "en-US") || voices[0];

      speechSynthesisUtterance.voice = preferredVoice;
      speechSynthesisUtterance.lang  = preferredVoice.lang;
      speechSynthesisUtterance.rate  = 1;   // default rate
      speechSynthesisUtterance.pitch = 1;   // default pitch

      ready_to_speak = true;
    }

    // Voices may arrive asynchronously
    setVoices();
    window.speechSynthesis.onvoiceschanged = setVoices;
  }

  /** Speak text using the prepared utterance (non-blocking). */
  function speak(text) {
    if (!ready_to_speak || !speechSynthesisUtterance || !text) return;

    ready_to_speak = false;
    speechSynthesisUtterance.text  = text;
    speechSynthesisUtterance.rate  = 0.8; // slightly slower for practice

    // window.speechSynthesis.cancel(); // uncomment if you want to cancel ongoing speech
    window.speechSynthesis.speak(speechSynthesisUtterance);

    speechSynthesisUtterance.onend   = () => { ready_to_speak = true; };
    speechSynthesisUtterance.onerror = () => { ready_to_speak = true; };
  }

  /* ================================= BOOT ================================ */
  main();
}
