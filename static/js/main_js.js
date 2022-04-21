URL = window.URL || window.webkitURL;

var gumStream; //variable dari getUserMedia()
var rec; // variable recorderjs
var input; 

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;

var recordButton = document.getElementById("button_record");
var stopButton = document.getElementById("button_stop");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
	console.log("button_record clicked");
    var constraints = { audio: true, video:false }

    // kalo lagi record stop button on
    recordButton.disabled = true;
	stopButton.disabled = false;

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

        gumStream = stream;
        audioContext = new AudioContext();

        // untuk update sample rate yang dibaca pake audio.sampleRate
        document.getElementById("sampleRate").innerHTML="Sample Rate =  1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input,{numChannels:1})

        rec.record()

		console.log("Recording started");
    }).catch(function(err) {
        // kalo ada gagal record buttonnya d enable lagi
    	recordButton.disabled = false;
    	stopButton.disabled = true;
	});

}

function stopRecording() {
	console.log("button_stop clicked");
    stopButton.disabled = true;
	recordButton.disabled = false;

    // ngestop record
    rec.stop();

    // nutup mic
    gumStream.getAudioTracks()[0].stop();


    // export audionya
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
	var filename = new Date().toISOString();
	var link = document.createElement('a');
	var au = document.createElement('audio');
	var li = document.createElement('li');

	au.controls = true;
	au.src = url;

    link.href = url;
	link.download = filename+".wav";
	link.innerHTML = "<br> Save to disk <br>";

	//add the new audio element to li
	li.appendChild(au);
	
	//add the filename to the li
	li.appendChild(document.createTextNode(filename))

	//add the save to disk link to li
	li.appendChild(link);

    //  lempar ke html pake js ke p id hasil
    var process = document.createElement('a');
	process.href="#";
	process.innerHTML = " Process " ;

    process.addEventListener("click", function(event){
		  var fd=new FormData();
		  fd.append("audio_data",blob, filename);
		  $.ajax({
	   	    type: "POST",
	   	    url: "/process",
	   	    data: fd,
	   	    processData: false,
            contentType: false,
	   	    success: function(data){
				try {
                	$('#hasil').html('U said = ' + data);
					// $('#feature_extraction').attr('src','image_feature.png');
					// document.getElementById("feature_extraction").src = "image_feature.jpg"
				} catch(err) {
					console.log("Error : " + err);
				}
				
	   	    }
	    });
	})
	li.appendChild(document.createTextNode (" "))//add a space in between
	li.appendChild(process)//add the upload link to li

	//add the li element to the ol
	recordingsList.appendChild(li);
}