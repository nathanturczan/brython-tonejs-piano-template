from browser import document, window, aio

log_el = document["log"]

def log(msg):
    log_el.text = log_el.text + str(msg) + "\n"

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
        # Slightly rolled chord
        window.PianoBridge.key_down("C4", 0.85, 0.00)
        window.PianoBridge.key_down("E4", 0.80, 0.03)
        window.PianoBridge.key_down("G4", 0.78, 0.06)

        window.PianoBridge.key_up("C4", 0.35)
        window.PianoBridge.key_up("E4", 0.35)
        window.PianoBridge.key_up("G4", 0.35)
    except Exception as e:
        log(f"Error playing: {e}")

document["start"].bind("click", start_and_load)
document["play"].bind("click", play_chord)

log("Ready. Click 'Start Audio + Load Piano'.")
