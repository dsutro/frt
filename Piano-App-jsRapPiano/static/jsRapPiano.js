const synth = new Tone.FMSynth({
	//harmonicity  : 3 ,
	modulationIndex  : 10 ,
	detune  : 0 ,
	harmonicity  : params.harmonicity ,  //ratio between carrier and modulator frequecny
	modulationIndex  : params.modulationIndex ,
	// detune  : params.detune ,
	oscillator  : {
	//type  : "sine"
	type  : params.car_type
	},
	envelope  : {
	//attack  : 0.01 ,
	// decay  : 0.01 ,
	// sustain  : 1 ,
	// release  : 0.5,
	attack  : params.amp_attack ,
	decay  : params.amp_decay ,
	sustain  : params.amp_sustain ,
	release  : params.amp_release
	}  ,
	modulation  : {
	// type  : "square"
	type : params.mod_type
	}  ,
	modulationEnvelope  : {
	// attack  : 0.5 ,
	// decay  : 0 ,
	// sustain  : 1 ,
	// release  : 0.5,
	attack  : params.mod_attack ,
	decay  : params.mod_decay ,
	sustain  : params.mod_sustain ,
	release  : params.mod_release
	}
});






// Set the tone to sine
//synth.oscillator.type = "sine";

//synth.oscillator.frequency = 900;
//synth.oscillator.modulationrequency = 3;

//synth.harmonicity.value = 10;

// connect it to the master output (your speakers)
synth.toDestination();

const piano = document.getElementById("piano");
console.log("hello");

let userOctave = 3;
$('#dis-user-oct').html(userOctave);
let note = "C"
note+=userOctave
console.log(note);

function calculateCorrectNote(user_input){
  let last_char = user_input[user_input.length-1];
  let correct_octave=userOctave+parseInt(last_char);
  let correct_note = user_input.replace(/.$/,correct_octave);
  console.log(correct_note);
  return correct_note;
}

piano.addEventListener("mousedown", e => {
  // fires off a note continously until trigger is released
	if(e.target.getAttribute('id') === 'z'){
		if (userOctave > 1){
			userOctave--;
		}
		$('#dis-user-oct').html(userOctave);
	}
	if(e.target.getAttribute('id') === 'x'){
		if (userOctave < 6){
			userOctave++;
		}
		$('#dis-user-oct').html(userOctave);
	}
	let correct_note = calculateCorrectNote(e.target.dataset.note);
	synth.triggerAttack(correct_note);
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
      	return synth.triggerAttack(calculateCorrectNote("C0"));
    case "w":
	  	document.getElementById('w').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("C#0"));
    case "s":
	  	document.getElementById('s').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("D0"));
    case "e":
	  	document.getElementById('e').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("D#0"));
    case "d":
	  	document.getElementById('d').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("E0"));
    case "f":
	  	document.getElementById('f').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("F0"));
    case "t":
	  	document.getElementById('t').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("F#0"));
    case "g":
	  	document.getElementById('g').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("G0"));
    case "y":
	  	document.getElementById('y').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("G#0"));
    case "h":
	  	document.getElementById('h').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("A0"));
    case "u":
	  	document.getElementById('u').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("A#0"));
    case "j":
	  	document.getElementById('j').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("B0"));
    case "k":
	  	document.getElementById('k').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("C1"));
    case "o":
	  	document.getElementById('o').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("C#1"));
    case "l":
	  	document.getElementById('l').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("D1"));
    case "p":
	  	document.getElementById('p').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("D#1"));
    case ";":
	  	document.getElementById(';').classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("E1"));
    case "'":
	  	document.getElementById("'").classList.add("active");
      	return synth.triggerAttack(calculateCorrectNote("F1"));
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
