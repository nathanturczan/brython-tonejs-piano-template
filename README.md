# Brython + Tone.js Salamander Piano Template

A minimal template for playing high-quality piano samples in a web browser using **Python** instead of JavaScript.

## What This Is

- **Brython** transpiles Python to JavaScript at runtime, so you write Python that runs in the browser
- **Tone.js** handles Web Audio
- **@tonejs/piano** loads the Salamander Grand Piano samples automatically from a CDN
- **tone_bridge.js** is a thin JavaScript wrapper (~30 lines) that exposes piano functions to Python

## Files

| File | Purpose |
|------|---------|
| `index.html` | HTML page that loads Tone.js and Brython from CDNs |
| `main.py` | Your Python code (runs in the browser via Brython) |
| `tone_bridge.js` | JS bridge exposing `key_down()` and `key_up()` to Python |

## How to Run

### Step 1: Clone the repo

```bash
git clone https://github.com/nathanturczan/brython-tonejs-piano-template.git
cd brython-tonejs-piano-template
```

### Step 2: Start a local server

You need a local server because browsers block ES modules loaded from `file://` URLs.

```bash
python3 -m http.server 8080
```

### Step 3: Open in browser

Open your browser and go to:

```
http://localhost:8080
```

### Step 4: Use the app

1. Click **"Start Audio + Load Piano"** (required - browsers block audio until user interaction)
2. Wait for "Salamander piano loaded." to appear in the log
3. Click **"Play C Major"** to hear a C major chord

## How to Use the Piano in Your Python Code

### Playing a single note

```python
from browser import window

# Press a key (note, velocity 0-1, delay in seconds)
window.PianoBridge.key_down("C4", 0.8, 0.0)

# Release the key (note, delay in seconds)
window.PianoBridge.key_up("C4", 0.5)
```

### Playing a chord

```python
# Stagger the notes slightly for a "rolled" feel
window.PianoBridge.key_down("C4", 0.85, 0.00)
window.PianoBridge.key_down("E4", 0.80, 0.03)
window.PianoBridge.key_down("G4", 0.78, 0.06)

# Release all notes
window.PianoBridge.key_up("C4", 0.5)
window.PianoBridge.key_up("E4", 0.5)
window.PianoBridge.key_up("G4", 0.5)
```

### Note format

Notes use scientific pitch notation:
- `"C4"` = middle C
- `"A4"` = 440 Hz
- `"F#3"`, `"Bb5"`, etc.

### Parameters

**`key_down(note, velocity, delaySeconds)`**
- `note`: string like `"C4"`, `"F#5"`
- `velocity`: 0.0 to 1.0 (how hard the key is struck)
- `delaySeconds`: seconds from now to play the note (0 = immediately)

**`key_up(note, delaySeconds)`**
- `note`: string like `"C4"`, `"F#5"`
- `delaySeconds`: seconds from now to release the note

## Initializing the Piano

Before playing notes, you must start the audio context and load the piano. This requires a user gesture (button click):

```python
from browser import window

async def start_and_load(ev):
    await window.Tone.start()           # Start Web Audio (requires user gesture)
    await window.PianoBridge.load_piano(velocities=5)  # Load Salamander samples
```

The `velocities` parameter (1-16) controls how many velocity layers are loaded. More = better dynamics but longer load time. 5 is a good balance.

## No Build Tools Required

This template uses no npm, no Vite, no webpack, no build system. Everything loads from CDNs:

- Tone.js from unpkg
- Brython from jsDelivr
- @tonejs/piano from unpkg
- Salamander samples from the @tonejs/piano CDN

Just serve the files and go.

## Troubleshooting

**"Piano not loaded" error**: Make sure you clicked "Start Audio + Load Piano" and waited for it to finish loading.

**No sound**: Check that your browser isn't muting the tab. Some browsers show a speaker icon you need to click.

**CORS errors**: Make sure you're using a local server (`python3 -m http.server`), not opening the HTML file directly.

## Credits

- [Tone.js](https://tonejs.github.io/) - Web Audio framework
- [@tonejs/piano](https://github.com/tambien/Piano) - Salamander Grand Piano wrapper
- [Brython](https://brython.info/) - Python in the browser
- [Salamander Grand Piano](https://archive.org/details/SalasmanderGrandPianoV3) - The actual piano samples
