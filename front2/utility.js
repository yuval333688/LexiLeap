// utility.js
window.utility = (function () {
  /** Save a number (or numeric string) to localStorage */
  function saveNumber(key, value) {
    if (value !== null && value !== undefined && value !== "") {
      localStorage.setItem(key, String(value)); // שמירה כמחרוזת
    } else {
      console.error("saveNumber: value is empty");
    }
  }

  /** Load a number from localStorage (or null if missing) */
  function loadNumber(key) {
    const val = localStorage.getItem(key);
    return val !== null ? Number(val) : null; 
  }

  /** (optional) Remove a saved number */
  function removeNumber(key) {
    localStorage.removeItem(key);
  }

  return { saveNumber, loadNumber, removeNumber };
})();
