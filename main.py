from browser import document, window, aio
import random

log_el = document["log"]

def log(msg):
    log_el.text = log_el.text + str(msg) + "\n"

# --- Ported from scale-navigator-dashboard ToneJS/Chord.js ---

# Random velocity between 0.2 and 0.6 (same as Dashboard)
def random_velocity():
    return 0.2 + random.random() * 0.4

# Max total roll duration in ms
MAX_ROLL_DURATION_MS = 500

# Fisher-Yates shuffle
def shuffle_array(arr):
    shuffled = arr[:]
    for i in range(len(shuffled) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

# Convert MIDI note number to note name (e.g., 60 -> "C4")
def midi_to_note_name(midi):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi // 12) - 1
    note_index = midi % 12
    return note_names[note_index] + str(octave)

def play_chord_rolled(midi_notes):
    """
    Play a chord with:
    - Random note order (shuffle)
    - Random delay per note (0 to MAX_ROLL_DURATION_MS)
    - Random velocity per note (0.2 to 0.6)
    """
    # Remove duplicates and shuffle
    unique_midi = list(set(midi_notes))
    shuffled_midi = shuffle_array(unique_midi)

    # Schedule each note with random delay
    for midi in shuffled_midi:
        note_name = midi_to_note_name(midi)
        delay_ms = random.random() * MAX_ROLL_DURATION_MS
        delay_sec = delay_ms / 1000.0
        velocity = random_velocity()

        # key_down with delay
        window.PianoBridge.key_down(note_name, velocity, delay_sec)

        # key_up after note has rung (delay + 1 second sustain)
        window.PianoBridge.key_up(note_name, delay_sec + 1.0)

# --- End ported logic ---

async def do_start_and_load():
    try:
        log("Starting audio context...")
        await aio.sleep(0)  # Yield to allow UI update

        # Start Tone.js audio context
        await window.Tone.start()
        log("Audio context started.")

        # Load the piano
        log("Loading Salamander piano samples...")
        await window.PianoBridge.load_piano()
        log("Salamander piano loaded.")

        document["play"].disabled = False
    except Exception as e:
        log(f"Error: {e}")

def start_and_load(ev):
    aio.run(do_start_and_load())

def play_chord(ev):
    try:
        # C major chord in MIDI (C4, E4, G4)
        c_major_midi = [60, 64, 67]
        play_chord_rolled(c_major_midi)
        log("Playing C major (rolled, randomized)")
    except Exception as e:
        log(f"Error playing: {e}")

document["start"].bind("click", start_and_load)
document["play"].bind("click", play_chord)

log("Ready. Click 'Start Audio + Load Piano'.")
