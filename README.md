# Terminal Wordle 🟩🟨⬛

A fully functional, duplicate-letter-safe Wordle clone built to run entirely in your computer's terminal.

## 🚀 How to Run
Make sure you have Python installed, then clone this repository and run:
\`\`\`bash
python wordle.py
\`\`\`

## 🧠 Game Logic Features
* **Two-Pass Validation:** Correctly evaluates duplicate letters so green matches take priority over yellow hints (matches official Wordle behavior).
* **Word Dictionary:** Validates guesses against an external `.txt` file containing over 140 000 five letter words.
* **Terminal Colors:** Uses ANSI escape codes for clean visual feedback directly in your command line.

## 🛠️ Built With
* Python 3