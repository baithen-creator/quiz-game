# Quiz Game

A simple Python quiz game with leaderboard tracking and intelligent answer matching.

## For Players
- Run: `python quiz_game.py` (multi-round quiz)
- Enter your name when prompted
- Complete each round and view individual scores
- Type "quit" at any time to exit
- View final total score and ranking on the leaderboard

## For Administrators

### Adding Questions
Edit `questions.txt` - one question per line in format:
```
Question text here|answer
```

### Multi-Round Quiz Setup (Default)
- **Create setup file**: Edit `quiz_setup.txt` with format: `Round Name|question_file.txt`
- **Run multi-round**: `python quiz_game.py` (default behavior)
- **Features**: Individual round scores, total score, combined leaderboard

### Sin[questions.txt](questions.txt)gle Round Quiz
- **Create question file**: Copy format from `questions.txt`
- **Run single round**: `python quiz_game.py questions.txt`
- **Custom single rounds**: `python quiz_game.py science_questions.txt`

### Managing Results
- **Clear leaderboard**: `python quiz_game.py --clear`
- **View results file**: Open `results.txt` (format: name|score)
- **Backup results**: Copy `results.txt` before clearing

### Answer Matching Features
- **Partial matching**: "Paris, France" matches "paris" (both directions)
- **Fuzzy matching**: Up to 2 character errors accepted ("jupitor" matches "jupiter")
- **Article removal**: "the murder" matches "murder"
- **Reverse partial**: "Ray Houghton" matches stored answer "Houghton"
- **Strict numeric**: Math answers must be exact

### Files
- `quiz_game.py` - Main game code
- `questions.txt` - Default quiz questions and answers
- `quiz_setup.txt` - Multi-round setup (optional)
- `results.txt` - Player scores (auto-created)
- `.env` - IDE configuration

## Troubleshooting
- If game won't start, ensure `quiz_setup.txt` exists for multi-round
- For single round, specify question file: `QuizGame.exe questions.txt`
- Empty `results.txt` is normal for new installations
- Use `--clear` flag to reset corrupted results file