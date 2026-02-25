import { Piano } from "https://esm.sh/@tonejs/piano@0.2.1";

let piano = null;

function ensureLoaded() {
  if (!piano) {
    throw new Error("Piano not loaded. Call load_piano() first.");
  }
}

window.PianoBridge = {

  async load_piano({ velocities = 5 } = {}) {
    if (!piano) {
      piano = new Piano({ velocities });
      piano.toDestination();
    }

    await piano.load(); // Loads Salamander samples from CDN
    return true;
  },

  key_down(note, velocity = 0.8, delaySeconds = 0.0) {
    ensureLoaded();
    piano.keyDown({
      note,
      velocity,
      time: window.Tone.now() + delaySeconds
    });
  },

  key_up(note, delaySeconds = 0.25) {
    ensureLoaded();
    piano.keyUp({
      note,
      time: window.Tone.now() + delaySeconds
    });
  }

};
