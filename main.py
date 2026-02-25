from browser import document, window

log_el = document["log"]

def log(msg):
    log_el.text = log_el.text + str(msg) + "\n"

async def start_and_load(ev):
    # Required user gesture for Web Audio
    await window.Tone.start()
    log("Audio context started.")

    await window.PianoBridge.load_piano(velocities=5)
    log("Salamander piano loaded.")

    document["play"].disabled = False

def play_chord(ev):
    # Slightly rolled chord
    window.PianoBridge.key_down("C4", 0.85, 0.00)
    window.PianoBridge.key_down("E4", 0.80, 0.03)
    window.PianoBridge.key_down("G4", 0.78, 0.06)

    window.PianoBridge.key_up("C4", 0.35)
    window.PianoBridge.key_up("E4", 0.35)
    window.PianoBridge.key_up("G4", 0.35)

document["start"].bind("click", start_and_load)
document["play"].bind("click", play_chord)

log("Ready. Click 'Start Audio + Load Piano'.")
