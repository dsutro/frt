
const synth = new Tone.FMSynth();
// Set the tone to sine
synth.oscillator.type = "triangle8";
// connect it to the master output (your speakers)
synth.toDestination();

const piano = document.getElementById("piano");
console.log("hello");

let userOctave = 4;
$('#dis-user-oct').html(userOctave);
let note = "C"
note+=userOctave
console.log(note);

piano.addEventListener("mousedown", e => {
  // fires off a note continously until trigger is released
	synth.triggerAttack(e.target.dataset.note);
	if(e.target.getAttribute('id') === 'z'){
		if (userOctave > 1){
			userOctave--;
		}
		$('#dis-user-oct').html(userOctave);
	}
	if(e.target.getAttribute('id') === 'x'){
		if (userOctave < 5){
			userOctave++;
		}
		$('#dis-user-oct').html(userOctave);
	}
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
	  	document.getElementById('a').classList.add("active");
      	return synth.triggerAttack(note);
    case "w":
	  	document.getElementById('w').classList.add("active");
      	return synth.triggerAttack("C#4");
    case "s":
	  	document.getElementById('s').classList.add("active");
      	return synth.triggerAttack("D4");
    case "e":
	  	document.getElementById('e').classList.add("active");
      	return synth.triggerAttack("D#4");
    case "d":
	  	document.getElementById('d').classList.add("active");
      	return synth.triggerAttack("E4");
    case "f":
	  	document.getElementById('f').classList.add("active");
      	return synth.triggerAttack("F4");
    case "t":
	  	document.getElementById('t').classList.add("active");
      	return synth.triggerAttack("F#4");
    case "g":
	  	document.getElementById('g').classList.add("active");
      	return synth.triggerAttack("G4");
    case "y":
	  	document.getElementById('y').classList.add("active");
      	return synth.triggerAttack("G#4");
    case "h":
	  	document.getElementById('h').classList.add("active");
      	return synth.triggerAttack("A4");
    case "u":
	  	document.getElementById('u').classList.add("active");
      	return synth.triggerAttack("A#4");
    case "j":
	  	document.getElementById('j').classList.add("active");
      	return synth.triggerAttack("B4");
    case "k":
	  	document.getElementById('k').classList.add("active");
      	return synth.triggerAttack("C5");
    case "o":
	  	document.getElementById('o').classList.add("active");
      	return synth.triggerAttack("C#5");
    case "l":
	  	document.getElementById('l').classList.add("active");
      	return synth.triggerAttack("D5");
    case "p":
	  	document.getElementById('p').classList.add("active");
      	return synth.triggerAttack("D#5");
    case ";":
	  	document.getElementById(';').classList.add("active");
      	return synth.triggerAttack("E5");
    case "'":
	  	document.getElementById("'").classList.add("active");
      	return synth.triggerAttack("F5");
	case "z":
		document.getElementById("z").classList.add("active");
		if (userOctave > 1){
			userOctave--;
		}
		$('#dis-user-oct').html(userOctave);
		return;
	case "x":
		document.getElementById("x").classList.add("active");
		if (userOctave < 5){
			userOctave++;
		}
		$('#dis-user-oct').html(userOctave);
		return;
    default:
      	return;
  }
});
// when the key is released, audio is released as well
document.addEventListener("keyup", e => {
  switch (e.key) {
    case "a":
		document.getElementById('a').classList.remove("active");
    case "w":
		document.getElementById('w').classList.remove("active");
    case "s":
		document.getElementById('s').classList.remove("active");
    case "e":
		document.getElementById('e').classList.remove("active");
    case "d":
		document.getElementById('d').classList.remove("active");
    case "f":
		document.getElementById('f').classList.remove("active");
    case "t":
		document.getElementById('t').classList.remove("active");
    case "g":
		document.getElementById('g').classList.remove("active");
    case "y":
		document.getElementById('y').classList.remove("active");
    case "h":
		document.getElementById('h').classList.remove("active");
    case "u":
		document.getElementById('u').classList.remove("active");
    case "j":
		document.getElementById('j').classList.remove("active");
    case "k":
		document.getElementById('k').classList.remove("active");
    case "o":
		document.getElementById('o').classList.remove("active");
    case "l":
		document.getElementById('l').classList.remove("active");
    case "p":
		document.getElementById('p').classList.remove("active");
    case ";":
		document.getElementById(';').classList.remove("active");
    case "'":
		document.getElementById("'").classList.remove("active");
		synth.triggerRelease(); 
	case "z":
		document.getElementById("z").classList.remove("active");
	case "x":
		document.getElementById("x").classList.remove("active");
  }
});
