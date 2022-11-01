
const synth = new Tone.FMSynth();
// Set the tone to sine
synth.oscillator.type = "triangle8";
// connect it to the master output (your speakers)
synth.toDestination();

const piano = document.getElementById("piano");
console.log("hello");

let userOctave = 4;
let note = "C"
note+=userOctave
console.log(note);

piano.addEventListener("mousedown", e => {
  // fires off a note continously until trigger is released
  synth.triggerAttack(e.target.dataset.note);
  //sampler.triggerAttack(e.target.dataset.note);
});

piano.addEventListener("mouseup", e => {
  // stops the trigger
  synth.triggerRelease();
  //sampler.triggerRelease();
});

// handles keyboard events
document.addEventListener("keydown", e => {
  // e object has the key property to tell which key was pressed
  switch (e.key) {
    case "a":
      return synth.triggerAttack(note);
    case "w":
      return synth.triggerAttack("C#4");
    case "s":
      return synth.triggerAttack("D4");
    case "e":
      return synth.triggerAttack("D#4");
    case "d":
      return synth.triggerAttack("E4");
    case "f":
      return synth.triggerAttack("F4");
    case "t":
      return synth.triggerAttack("F#4");
    case "g":
      return synth.triggerAttack("G4");
    case "y":
      return synth.triggerAttack("G#4");
    case "h":
      return synth.triggerAttack("A4");
    case "u":
      return synth.triggerAttack("A#4");
    case "j":
      return synth.triggerAttack("B4");
    case "k":
      return synth.triggerAttack("C5");
    case "o":
      return synth.triggerAttack("C#5");
    case "l":
      return synth.triggerAttack("D5");
    case "p":
      return synth.triggerAttack("D#5");
    case ";":
      return synth.triggerAttack("E5");
    case "'":
      return synth.triggerAttack("F5");
    default:
      return;
  }
});
// when the key is released, audio is released as well
document.addEventListener("keyup", e => {
  switch (e.key) {
    case "a":
    case "w":
    case "s":
    case "e":
    case "d":
    case "f":
    case "t":
    case "g":
    case "y":
    case "h":
    case "u":
    case "j":
    case "k":
    case "o":
    case "l":
    case "p":
    case ";":
    case "'":
       synth.triggerRelease(); 
  }
});
