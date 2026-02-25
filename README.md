# Brython + Tone.js Salamander Piano Template

A minimal template for playing high-quality piano samples in a web browser using **Python** instead of JavaScript.

## What This Is

- **Brython** transpiles Python to JavaScript at runtime, so you write Python that runs in the browser
- **Tone.js** handles Web Audio
- **Tone.Sampler** loads Salamander Grand Piano MP3s from `tonejs.github.io/audio/salamander/`
- **tone_bridge.js** is a thin JavaScript wrapper (~60 lines) that exposes piano functions to Python

## Files

| File | Purpose |
|------|---------|
| `index.html` | HTML page that loads Tone.js and Brython from CDNs |
| `main.py` | Your Python code (runs in the browser via Brython) |
| `tone_bridge.js` | JS bridge exposing `key_down()`, `key_up()`, and `load_piano()` to Python |

## How to Run

### Step 1: Clone the repo

```bash
git clone https://github.com/nathanturczan/brython-tonejs-piano-template.git
cd brython-tonejs-piano-template
```

### Step 2: Start a local server

```bash
python3 -m http.server 8080
```

### Step 3: Open in browser

```
http://localhost:8080
```

### Step 4: Use the app

1. Click **"Start Audio + Load Piano"** first (required - browsers block audio until user interaction)
2. Wait for "Salamander piano loaded." to appear in the log
3. Click **"Play C Acoustic"** to hear a rolled chord

## How to Use the Piano in Your Python Code

### Playing a single note

```python
from browser import window

# Press a key (note, velocity 0-1, delay in seconds)
window.PianoBridge.key_down("C4", 0.8, 0.0)

# Release the key (note, delay in seconds)
window.PianoBridge.key_up("C4", 0.5)
```

### Playing a rolled chord (like the template does)

```python
import random

def shuffle_array(arr):
    shuffled = arr[:]
    for i in range(len(shuffled) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

def midi_to_note_name(midi):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi // 12) - 1
    return note_names[midi % 12] + str(octave)

# C acoustic voicing: C2, G2, E3, Bb3, D4, F#4, A4
midi_notes = [36, 43, 52, 58, 62, 66, 69]
shuffled = shuffle_array(midi_notes)

for midi in shuffled:
    note = midi_to_note_name(midi)
    delay = random.random() * 1.5      # 0-1.5 second roll
    velocity = 0.2 + random.random() * 0.4  # 0.2-0.6

    window.PianoBridge.key_down(note, velocity, delay)
    window.PianoBridge.key_up(note, delay + 10.0)  # 10 second sustain
```

### Note format

Notes use scientific pitch notation:
- `"C4"` = middle C (MIDI 60)
- `"A4"` = 440 Hz (MIDI 69)
- `"F#3"`, `"Bb5"`, etc.

### Parameters

**`key_down(note, velocity, delaySeconds)`**
- `note`: string like `"C4"`, `"F#5"`
- `velocity`: 0.0 to 1.0 (scales volume)
- `delaySeconds`: seconds from now to play the note (0 = immediately)

**`key_up(note, delaySeconds)`**
- `note`: string like `"C4"`, `"F#5"`
- `delaySeconds`: seconds from now to release the note

**`load_piano()`**
- No parameters. Loads 30 Salamander samples covering the full range.

## Initializing the Piano

Before playing notes, you must start the audio context and load the piano. This requires a user gesture (button click):

```python
from browser import window, aio

async def start_and_load(ev):
    await window.Tone.start()        # Start Web Audio (requires user gesture)
    await window.PianoBridge.load_piano()  # Load Salamander samples
```

## No Build Tools Required

This template uses no npm, no Vite, no webpack, no build system. Everything loads from CDNs:

- Tone.js v14.8.49 from unpkg
- Brython v3.11.3 from jsDelivr
- Salamander samples from tonejs.github.io

Just serve the files and go.

## Troubleshooting

**"Piano not loaded" error**: Make sure you clicked "Start Audio + Load Piano" and waited for it to finish loading.

**No sound**: Check that your browser isn't muting the tab. Some browsers show a speaker icon you need to click.

**CORS errors**: Make sure you're using a local server (`python3 -m http.server`), not opening the HTML file directly.

## Credits

- [Tone.js](https://tonejs.github.io/) - Web Audio framework
- [Brython](https://brython.info/) - Python in the browser
- [Salamander Grand Piano](https://archive.org/details/SalasmanderGrandPianoV3) - The piano samples (hosted at tonejs.github.io)
