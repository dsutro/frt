$(window).resize(function () {
	$('.rapPiano').each(function () {
		this.Render();
	});
});

function myfunction(x) {

    const data = x;
    const dict_values = {data} //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    $.ajax({
        url:"/test",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s)});
}

(function ($) {
	$.fn.jsRapPiano = function (options) {

		return this.each(function () {
			this.opt = $.extend({
				octave: 3,
				octaves: 2,
				tuning: 440,
				waveType: 'string',
				envelope: {
					attack: 0.1,
					decay: 0.1,
					sustain: 0.1,
					release: 0.5,
					level: 0.5
				},
				onClick: null
			}, options);

			let base = this;
			let AudioContext = window.AudioContext || window.webkitAudioContext;
			this.audioContext = new AudioContext();
			this.oscillator = this.audioContext.createOscillator();
			this.gainMain = this.audioContext.createGain();
			this.gainMain.gain.value = 1;
			this.gainMain.connect(this.audioContext.destination);
			this.oscillator.start(0);
			this.oscillator.type = this.opt.waveType;

			const compKey = ['A','W','S','E','D','F','T','G','Y','H','U','J','K','O','L','P',':','"',];
			const keyID = [65,87,83,69,68,70,84,71,89,72,85,74,75,79,76,80,186,222,];

			this.Render = function () {
				$(this).empty();
				let w = $(this).width();
				w = w / (this.opt.octaves * 15);
				$(this).addClass('rapPiano').height(w * 3);
				let i = 12 * (this.opt.octave + 1);
				for (let o = 0; o < this.opt.octaves; o++) {
					let counter = 0;
					let counterid = 0;
					for (let x = 0; x < 11; x++) {
						let k = $('<div>').addClass('divKey').css({ width: w }).appendTo(this);
						$('<div>').addClass('major').attr('id','id'+keyID[counterid++]).append("<span class='maLetter'>"+compKey[counter++]+"</span>").prop('index', i++).appendTo(k);
						if ((x % 11 == 2) || (x % 11 == 6) || (x % 11 == 9) || (x % 11 == 10)) continue;
						$('<div>').addClass('minor').attr('id','id'+keyID[counterid++]).append("<span class='miLetter'>"+compKey[counter++]+"</span>").prop('index', i++).appendTo(k);
					}
				}
				$('.major,.minor', this).on({
					mousedown: function (e) {
						console.log(e);
						let i = $(this).prop('index');
						let f = base.opt.tuning*2;
						base.audioContext.resume();
						myfunction(i);
						fetch('/sound_feed')
						  .then(response => response.json())
						  .then(data => base.PlaySound(f*data["sound"]))




						if (base.opt.onClick)
							base.opt.onClick.call(base, i, f);
					},
					// keydown: function(e){
					// 	let di = $("#id"+e.keyCode);
					// 	console.log(di);
					// 	di.css("backgroundColor", "red");
					// 	let i = $(this).prop('index');
					// 	let f = base.opt.tuning*2;
					// 	base.audioContext.resume();
					// 	myfunction(i);
					// 	fetch('/sound_feed')
					// 	  .then(response => response.json())
					// 	  .then(data => base.PlaySound(f*data["sound"]))
					// }
				});
				$(document).keydown(function(e){
						let di = $("#id"+e.keyCode);
						console.log(di);
						di.css("backgroundColor", "red");
						let i = $(this).prop('index');
						let f = base.opt.tuning*2;
						base.audioContext.resume();
						myfunction(i);
						fetch('/sound_feed')
						  .then(response => response.json())
						  .then(data => base.PlaySound(f*data["sound"]))
				});
			}

			this.PlaySound = function (frequency) {
				let t = this.audioContext.currentTime;
				gainNode = this.audioContext.createGain();
				gainNode.connect(this.gainMain);
				this.oscillator.connect(gainNode);
				gainNode.gain.setValueAtTime(0, t);
				this.oscillator.frequency.value = frequency;
				t += this.opt.envelope.attack;
				gainNode.gain.linearRampToValueAtTime(1, t);
				t += this.opt.envelope.decay;
				gainNode.gain.linearRampToValueAtTime(this.opt.envelope.level, t);
				t += this.opt.envelope.sustain;
				gainNode.gain.linearRampToValueAtTime(this.opt.envelope.level, t);
				t += this.opt.envelope.release;
				gainNode.gain.linearRampToValueAtTime(0, t);
			}

			this.Render();

		})

	}
})(jQuery);
