const video = document.getElementById("video");
var model;

let localStream;
let peerConnection;
let remoteVideo;
let serverConnection;
let uuid;
var fps;
const HOST = location.origin.replace(/^http/, 'ws') + location.pathname;

var ctx;
const font = "16px sans-serif";
var prevTime;
var pastFrameTimes = [];

const peerConnectionConfig = {
    'iceServers': [
        {'urls': 'stun:stun.stunprotocol.org:3478'},
        {'urls': 'stun:stun.l.google.com:19302'},
    ]
};

createShareLink();

function start(isCaller) {
    peerConnection = new RTCPeerConnection(peerConnectionConfig);
    peerConnection.onicecandidate = gotIceCandidate;
    peerConnection.ontrack = gotRemoteStream;

    for(const track of localStream.getTracks()) {
        peerConnection.addTrack(track, localStream);
    }

    if(isCaller) {
        peerConnection.createOffer().then(createdDescription).catch(errorHandler);
    }
}

function gotIceCandidate(event) {
    if(event.candidate != null) {
        serverConnection.send(JSON.stringify({'ice': event.candidate, 'uuid': uuid}));
    }
}

function createdDescription(description) {
    console.log('got description');

    peerConnection.setLocalDescription(description).then(() => {
        serverConnection.send(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid}));
    }).catch(errorHandler);
}

function gotRemoteStream(event) {
    console.log('got remote stream');
    remoteVideo.srcObject = event.streams[0];
    document.getElementById("findOpponent").style.display = "none";
}

function errorHandler(error) {
    console.log(error);
}

function createUUID() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
    }

    return `${s4() + s4()}-${s4()}-${s4()}-${s4()}-${s4() + s4() + s4()}`;
}

function sendAction(action) {
    if(gameState.is_playing) {
        serverConnection.send(JSON.stringify({'command': "updateGameState", 'action': action}));
    }
}

// Function to start the video stream
function startVideoStream() {

    uuid = createUUID();

    serverConnection = new WebSocket(HOST);

    serverConnection.onopen = () => {
        const connectCommand = {
            command: 'connect',
            uuid: uuid,
            room: location.pathname,
        };
        serverConnection.send(JSON.stringify(connectCommand));
    };
    
    serverConnection.onmessage = function (message) {
        if(message.data === 'Room is full') {
            window.location.href = '/?f=t';
        } else if(message.data == "All rooms are empty :(") {
            alert("All rooms are empty :(");
        } else {
            gotMessageFromServer(message);
        }
    };

    remoteVideo = document.getElementById('remoteVideo');

    return navigator.mediaDevices
    .getUserMedia({
        audio: false,
        video: true
    })
    .then(function (stream) {
        return new Promise(function (resolve) {
            localStream = stream;
            video.srcObject = stream;
            video.onloadeddata = function () {
                video.play();
                resolve();
            };
        });
    });
}

function initializeGame(){
    Promise.all([startVideoStream(), loadModelPromise]).then(function () {
        document.getElementById('webcam').style.display = "none";
        resizeCanvas();
        detectFrame();
        start(true);
        document.getElementById("findOpponent").style.display = "block";
    });
}

function videoDimensions(video) {
    // Ratio of the video's intrinsic dimensions
    var videoRatio = video.videoWidth / video.videoHeight;

    // The width and height of the video element
    var width = video.offsetWidth,
        height = video.offsetHeight;

    // The ratio of the element's width to its height
    var elementRatio = width / height;

    // If the video element is short and wide
    if (elementRatio > videoRatio) {
        width = height * videoRatio;
    } else {
        // It must be tall and thin, or exactly equal to the original ratio
        height = width / videoRatio;
    }

    return {
        width: width,
        height: height
    };
}

window.onresize = function() {
    resizeCanvas();
};

const resizeCanvas = function () {
    var canvas = document.getElementById("canvas");

    ctx = canvas.getContext("2d");
    

    var dimensions = videoDimensions(video);

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    canvas.style.width = dimensions.width + "px";
    canvas.style.height = dimensions.height + "px";
    canvas.style.left = "0px";
};

const detectFrame = function () {
    if (!model) {
        return requestAnimationFrame(detectFrame);
    } 

    model
        .detect(video)
        .then(function (predictions) {
            requestAnimationFrame(detectFrame);
            renderPredictions(predictions);

            if (prevTime) {
                pastFrameTimes.push(Date.now() - prevTime);
                if (pastFrameTimes.length > 30) pastFrameTimes.shift();

                var total = 0;
                _.each(pastFrameTimes, function (t) {
                    total += t
                    total += t / 1000;
                });

                fps = Math.round(pastFrameTimes.length / total);
            }
            prevTime = Date.now();
        })
        .catch(function (e) {
            console.log("CAUGHT", e);
            requestAnimationFrame(detectFrame);
        });
};

function createShareLink() {
    document.getElementById("shareLink").innerHTML = location.origin + location.pathname;
}

function joinStrangerRoom() {
    serverConnection.send(JSON.stringify({ command: 'getOldestRoomWithOnePerson' }));
}

function joinRoom(path) {
    let currentUrl = new URL(window.location.href);
    let resultUrl = `${currentUrl.origin}${currentUrl.pathname.split('/').slice(0, 3).join('/')}`;

    window.location.href = resultUrl + path + '/';
}

function checkUrlVariableS(url) {
    const parsedUrl = new URL(url);
    const searchParams = new URLSearchParams(parsedUrl.search);
    return searchParams.get('s') === 't';
}

if (checkUrlVariableS(window.location.href)) {
    initializeGame();
}