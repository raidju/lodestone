# Instrument Practice App

A desktop app that helps people practice an instrument: a tuner, play-along charts built from songs they choose, and a practice mode that scores timing and pitch.


## What it is

The app takes a song the user already has, removes the instrument they want to learn, and turns that instrument's part into a chart they can read. They then play along with the rest of the band while the app listens and scores how close they were, note by note.

It runs on a laptop with no internet connection. Input is a microphone or a USB instrument cable.


## !!!!!! How to Run !!!!!!!

You need [uv](https://docs.astral.sh/uv/) **0.12.19 or newer**. Older versions skip part of the project config and fail with a confusing TensorFlow error.

```bash
git clone <repo-url>
cd <repo-folder>
uv sync --locked      # installs Python 3.12 and every dependency from uv.lock
uv run pytest         # runs the tests
```

`--locked` makes the install fail with a noti if `uv.lock` is out of date instead of quietly changing versions.

## Workflow

1. Pick an issue from the project board, or open one, or just tell somone what you're working on so we're kinda coordnated
2. Branch off `main`, one branch per change.
3. Please dont commit directly to `main`.

## Features
most likely will change rough draft for now
Core features should be completed by the February state competition.

| Feature | What the user gets | Priority |
| --- | --- | --- |
| Tuner | Live note name and how many cents sharp or flat each string is | Core |
| Song import | Load an `.mp3`, `.wav` or `.mp4` they already own | Core |
| Backing track | The song with their instrument taken out, to play along with | Core |
| Auto chart | The instrument's notes written out as a chart; for guitar, tab with string and fret | Core |
| Play-along | Backing track plays while the chart scrolls under a play line | Core |
| Scoring | A percentage for notes hit, plus how early or late each note was | Core |
| Calibration | A short tap test so timing grades are fair on any laptop and mic | Core |
| Section looping | Repeat one hard part and score each pass | Core |
| Chord scoring | Checks every note in a chord instead of just one | Stretch |
| Chart editor | Fix notes the auto chart got wrong | Stretch |
| Piano mode | A note-lane view for piano; separation quality needs testing first | Stretch |
| MIDI keyboard input | Score a plugged-in keyboard directly | Stretch |
| Slow-down practice | Play along at reduced speed | Stretch |
| Alternate tunings | Drop D, open G and others | Stretch |

**Out of scope:** streaming services like Spotify. Their developer policy forbids analyzing their audio. Users import files they already own instead.

## Libraries

Only Python and uv are installed by hand. Everything else comes from `uv.lock`, which holds the exact versions.

| Library | Used for |
| --- | --- |
| Python 3.12 | The language, pinned in `.python-version` |
| [uv](https://docs.astral.sh/uv/) | Installs everything from the lockfile |
| [Demucs](https://github.com/adefossez/demucs) | Splits a song into separate instruments (runs on torch) |
| [Basic Pitch](https://github.com/spotify/basic-pitch) | Turns the separated instrument into notes (runs on onnxruntime) |
| [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) | Pulls audio out of `.mp3` and `.mp4` files; bundles ffmpeg |
| [sounddevice](https://python-sounddevice.readthedocs.io/) | Plays the backing track and records the mic at the same time |
| [soundfile](https://python-soundfile.readthedocs.io/) | Reads and writes WAV files |
| [numpy](https://numpy.org/) | Math for the pitch detector |
| [librosa](https://librosa.org/) | Audio helpers; a reference to check the pitch detector against |
| [mir_eval](https://github.com/mir-evaluation/mir_eval) | Measures transcription accuracy in tests |

UI framework: not chosen yet.

### Written from scratch

These parts are small and will be built by us instead of pulled from a library:

- **Pitch detector (YIN):** hears which note is being played. The existing library options don't install reliably on Windows.
- **Note-start detection:** tells one held note apart from two repeated notes.
- **String and fret assignment:** picks where on the neck each note should be played.
- **Scoring:** matches played notes to the chart and grades them.

## Constraints

- Works with no internet connection. Everything it needs is downloaded during setup.
- Works the same on Windows and Apple Silicon Macs.
