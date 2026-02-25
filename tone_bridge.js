// Salamander Grand Piano samples (same as Ensemble-Jammer)
const PIANO_SAMPLES_BASE = "https://tonejs.github.io/audio/salamander/";
const PIANO_SAMPLE_NOTES = [
  "A0", "C1", "D#1", "F#1", "A1", "C2", "D#2", "F#2", "A2", "C3", "D#3", "F#3",
  "A3", "C4", "D#4", "F#4", "A4", "C5", "D#5", "F#5", "A5", "C6", "D#6", "F#6",
  "A6", "C7", "D#7", "F#7", "A7", "C8"
];

function buildPianoSamples() {
  const samples = {};
  for (const note of PIANO_SAMPLE_NOTES) {
    samples[note] = `${PIANO_SAMPLES_BASE}${note.replace("#", "s")}.mp3`;
  }
  return samples;
}

let sampler = null;
let isLoaded = false;

function ensureLoaded() {
  if (!isLoaded) {
    throw new Error("Piano not loaded. Call load_piano() first.");
  }
}

window.PianoBridge = {

  async load_piano() {
    if (sampler && isLoaded) {
      return true;
    }

    return new Promise((resolve, reject) => {
      sampler = new Tone.Sampler({
        urls: buildPianoSamples(),
        release: 1.5,
        onload: () => {
          isLoaded = true;
          sampler.toDestination();
          resolve(true);
        },
        onerror: (e) => {
          reject(e);
        }
      });
    });
  },

  key_down(note, velocity = 0.8, delaySeconds = 0.0) {
    ensureLoaded();
    const time = Tone.now() + delaySeconds;
    sampler.triggerAttack(note, time, velocity);
  },

  key_up(note, delaySeconds = 0.25) {
    ensureLoaded();
    const time = Tone.now() + delaySeconds;
    sampler.triggerRelease(note, time);
  }

};
