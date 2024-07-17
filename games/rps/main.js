var publishable_key = "YOUR_ROBOFLOW_KEY_HERE";
var toLoad = {
    model: "rock-paper-scissors-sxsw",
    version: 11,
};

var loadModelPromise = new Promise(function (resolve, reject) {
    roboflow
        .auth({
            publishable_key: publishable_key
        })
        .load(toLoad)
        .then(function (m) {
            model = m;
            model.configure({
                threshold: 0.20,
                overlap: 0.3,
                max_objects: 2
            });
            resolve();
        });
});

function gotMessageFromServer(message) {
    if(!peerConnection) start(false);

    const signal = JSON.parse(message.data);

    // Ignore messages from yourself
    if(signal.uuid == uuid) return;

    if(signal.sdp) {
        peerConnection.setRemoteDescription(new RTCSessionDescription(signal.sdp)).then(() => {
        // Only create answers in response to offers
        if(signal.sdp.type !== 'offer') return;

        peerConnection.createAnswer().then(createdDescription).catch(errorHandler);
        }).catch(errorHandler);
    } else if(signal.ice) {
        peerConnection.addIceCandidate(new RTCIceCandidate(signal.ice)).catch(errorHandler);
    }

    if (signal.room) {
        window.location.href = signal.room + "?s=t";
    }

    if(signal.newRoom) {
        joinRoom(signal.newRoom);
    }

    if(signal.gameState) {
        resolveRound(signal.gameState);
    }
}

const renderPredictions = function (predictions) {

    var dimensions = videoDimensions(video);
    var scale = 1;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    predictions.forEach(function (prediction) {

            
        const x = prediction.bbox.x;
        const y = prediction.bbox.y;
        const width = prediction.bbox.width;
        const height = prediction.bbox.height;

        // Draw the bounding box.
        ctx.strokeStyle = prediction.color;
        ctx.lineWidth = 4;
        ctx.strokeRect(
            (x - width / 2) / scale,
            (y - height / 2) / scale,
            width / scale,
            height / scale
        );

        // Draw the label background.
        ctx.fillStyle = prediction.color;
        const textWidth = ctx.measureText(prediction.class).width;
        const textHeight = parseInt(font, 10); // base 10
        ctx.fillRect(
            (x - width / 2) / scale,
            (y - height / 2) / scale,
            textWidth + 8,
            textHeight + 4
        );

        gameState.yourCurrentPrediction = prediction.class.toUpperCase();
        sendAction(gameState.yourCurrentPrediction);
    });

    predictions.forEach(function (prediction) {
        const x = prediction.bbox.x;
        const y = prediction.bbox.y;
        const width = prediction.bbox.width;
        const height = prediction.bbox.height;

        // Draw the text last to ensure it's on top.
        ctx.font = font;
        ctx.textBaseline = "top";
        ctx.fillStyle = "#000000";
        ctx.fillText(
            prediction.class,
            (x - width / 2) / scale + 4,
            (y - height / 2) / scale + 1
        );
    });

    document.getElementById("move_you").innerHTML = "You: " + gameState.yourCurrentPrediction;
};
