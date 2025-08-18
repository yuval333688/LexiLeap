# lessons_fs.py
from pathlib import Path
import re

class LessonsFS:
    """
    Reads a single lesson TXT file from '../lessens'.
    File name format: lesson{N}.txt (e.g., lesson0.txt).
    Returns JSON-friendly dict with both raw text and a tokenized word list.
    """

    @staticmethod
    def read_lesson(num: int) -> dict:
        """
        Returns:
        {
          "level": <num>,
          "text": "<raw file content>",
          "words": ["word1", "word2", ...]
        }
        """
        path = Path("lessens") / f"lesson{num}.txt"
        if not path.exists():
            return {"level": num, "text": "", "words": []}

        text = path.read_text(encoding="utf-8")
        words = re.findall(r"\S+", text)
        return {"level": num, "text": text, "words": words}
