## Quick context

This repository is a small Telegram bot implemented in a single script: `bot.py`.
Its purpose: deliver a US/UK glossary (list of word entries) and optional TTS voice messages using gTTS/pydub. The bot runs with python-telegram-bot in polling mode.

## Big picture (what to know)

- Single-entry point: `bot.py` (no package layout). All core logic lives here: data (`GLOSSARY`), formatting (`format_word_entry`), TTS (`speak_word`) and Telegram handlers (`start`, `help_command`, `random_word`, `word_by_number`).
- Data flow: `GLOSSARY` (list of dicts) → pick entry (random or by id) → `format_word_entry` (Markdown text) → `speak_word` (optional audio file) → Telegram send (text + voice/audio).
- External deps are optional at runtime: imports use `importlib` and fall back gracefully if modules are missing (gTTS, pydub, python-telegram-bot). Code paths handle missing deps by skipping voice or failing early with a logged message.

## Key files / locations

- `bot.py` — the only (canonical) source file. Edit here for any behavior change.

## Important runtime / developer workflows

- Installing runtime deps (recommended):

  pip install python-telegram-bot gTTS pydub ffmpeg-python

- Platform note: `pydub` relies on an external `ffmpeg` binary. On Windows ensure `ffmpeg.exe` is installed and on PATH (download from ffmpeg.org or install via Chocolatey).

- Running locally (PowerShell example):

  $env:TELEGRAM_TOKEN = "<your-telegram-token>"; python bot.py

  The script reads `TELEGRAM_TOKEN` from the environment (main checks it and exits if missing). Do not hard-code production tokens in the file.

## Project-specific patterns and examples

- GLOSSARY shape: each item is a dict with keys used by the code: `id`, `us`, `uk`, `us_pr`, `uk_pr`, `ru`. Example entry from the file:

  {"id":1,"us":"color","uk":"colour","us_pr":"ˈkʌlər","uk_pr":"ˈkʌlə","ru":"цвет"}

- ID lookup: `get_word_by_id` performs a linear search over `GLOSSARY`. Keep IDs unique and small; if you change to an indexed store, update callers accordingly.

- TTS and audio handling: `speak_word(text, lang="en")` uses gTTS to write an MP3 to a temp file and — if `pydub.AudioSegment` is available — converts to OGG and deletes the intermediate MP3. The function returns a file path or None on failure. Caller (`send_word_entry`) opens and sends the file and then deletes it.

- Telegram send fallbacks: `send_word_entry` first tries `update.message.reply_markdown(...)` and falls back to `reply_text` on exceptions. For audio it chooses `reply_voice` for `.ogg` and `reply_audio` otherwise.

- Handler registration example (how to add a command):

  dp.add_handler(CommandHandler("mycmd", my_handler))

  See `main()` for where `Updater` and `dispatcher` are wired (polling mode: `updater.start_polling()`). If you change to webhooks, update startup/shutdown logic.

## What to watch for when editing

- Keep the dynamic-import fallback pattern intact if you expect the bot to run in environments without all optional deps. Many code paths assume missing deps and only log warnings — changing that may break local development workflows.
- When modifying audio code, remember Windows needs ffmpeg in PATH; tests or local runs will fail silently if pydub+ffmpeg are missing (the code logs warnings). If you add unit tests that exercise audio conversion, mock `gTTS`/`AudioSegment` or require ffmpeg in CI.
- `format_word_entry` returns Markdown-formatted text — changes here affect how messages render. Some Telegram client versions differ in supported markdown methods; the code already uses a try/except fallback.

## Examples you can copy-paste

- Add a new bot command that replies with the first glossary item:

  def first_item(update, context):
      send_word_entry(update, context, GLOSSARY[0])

  dp.add_handler(CommandHandler("first", first_item))

- Replace GLOSSARY with an external JSON file (minimal example):

  import json
  with open("glossary.json", "r", encoding="utf-8") as f:
      GLOSSARY = json.load(f)

  Keep the same dict shape (id/us/uk/us_pr/uk_pr/ru) to remain compatible.

## Known assumptions (discoverable from code)

- Bot runs in polling mode using `Updater` from python-telegram-bot.
- Environment variable `TELEGRAM_TOKEN` is required at runtime (main() enforces this).
- Audio generation is optional; absence of `gTTS` or `pydub` does not prevent basic text functionality.

## Quick checklist for contributors / AI edits

- If adding new commands: update `dp.add_handler(...)` in `main()`.
- If changing message formatting: update `format_word_entry` and re-check both Markdown and plaintext fallbacks.
- If changing audio flow: update `speak_word` and ensure temporary files are cleaned (the code currently attempts removal in finally blocks).

---

If any of these sections are unclear or you want the instructions expanded (examples for CI, tests, or webhook deployment), tell me what to prioritize and I'll update this file.
