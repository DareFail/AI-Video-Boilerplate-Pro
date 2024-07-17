'use strict';

const WebSocket = require('ws');

const defaultGameState_007 = {
  id_p1: "",
  id_p2: "",
  health_p1: 3,
  health_p2: 3,
  move_p1: 'NOTHING',
  move_p2: 'NOTHING',
  videoMove_p1: "",
  videoMove_p2: "",
  bullets_p1: 1,
  bullets_p2: 1,
  is_resolving: false,
  remoteVideoVisible: false,
  end_game: false,
  gameStateText: "",
  winnerText_p1: "",
  winnerText_p2: "",
  is_playing: true
};





function handleRound_007(gameStates, ws, clients) {

    if (gameStates[ws.room].move_p1 == "SHOOT") {
        if (gameStates[ws.room].bullets_p1 <= 0) {
            gameStates[ws.room].move_p1 = "TRY TO SHOOT, NO BULLETS!";
            gameStates[ws.room].videoMove_p1 = "NO BULLETS!";
        } else {
            gameStates[ws.room].bullets_p1 = gameStates[ws.room].bullets_p1 - 1;
            if (gameStates[ws.room].move_p2 != "BLOCK") {
                gameStates[ws.room].health_p2 = gameStates[ws.room].health_p2 - 1;
            }
        }
    }
    if (gameStates[ws.room].move_p2 == "SHOOT") {
        if (gameStates[ws.room].bullets_p2 <= 0) {
            gameStates[ws.room].move_p2 = "TRY TO SHOOT, NO BULLETS!";
            gameStates[ws.room].videoMove_p2 = "NO BULLETS!";
        } else {
            gameStates[ws.room].bullets_p2 = gameStates[ws.room].bullets_p2 - 1;
            if (gameStates[ws.room].move_p1 != "BLOCK") {
                gameStates[ws.room].health_p1 = gameStates[ws.room].health_p1 - 1;
            }
        }
    }
    

    if (gameStates[ws.room].health_p1 <= 0 || gameStates[ws.room].health_p2 <= 0) {
        gameStates[ws.room].end_game = true;
        if (gameStates[ws.room].health_p1 > 0) {
            gameStates[ws.room].winnerText_p1 = "WINNER!"
            gameStates[ws.room].winnerText_p2 = "DEFEAT!"
        } else if (gameStates[ws.room].health_p2 > 0) {
            gameStates[ws.room].winnerText_p1 = "DEFEAT!"
            gameStates[ws.room].winnerText_p2 = "WINNER!"
        } else {
            gameStates[ws.room].winnerText_p1 = "DRAW!"
            gameStates[ws.room].winnerText_p2 = "DRAW!"
        }
        broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
    } else {
        if (gameStates[ws.room].move_p1 == "RELOAD") {
            gameStates[ws.room].bullets_p1 = gameStates[ws.room].bullets_p1 + 1;
        }
        if (gameStates[ws.room].move_p2 == "RELOAD") {
            gameStates[ws.room].bullets_p2 = gameStates[ws.room].bullets_p2 + 1;
        }
    }
  
}





function roundLoop_007(gameStates, ws, clients) {
    gameStates[ws.room].remoteVideoVisible = false;
    broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
    setTimeout(() => {
        gameStates[ws.room].gameStateText = "1";
        broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
        setTimeout(() => {
            gameStates[ws.room].gameStateText = "1, 2";
            broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
            setTimeout(() => {
                gameStates[ws.room].gameStateText = "1, 2, Go!";
                gameStates[ws.room].is_resolving = true;
                gameStates[ws.room].remoteVideoVisible = true;
                handleRound_007(gameStates, ws, clients);
                broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
                if(!gameStates[ws.room].end_game) {
                    setTimeout(() => { 
                        roundLoop_007(gameStates, ws, clients);
                        gameStates[ws.room].gameStateText = "";
                        gameStates[ws.room].is_resolving = false;
                        broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
                    }, 2000);
                }
                broadcast_game_007(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
            }, 2000);
        }, 2000);
    }, 2000);
}







function update_007(gameStates, newMove, ws) {
    if (!gameStates[ws.room].is_resolving || gameStates[ws.room].move_p1 == "NOTHING") {
        if (ws.uuid === gameStates[ws.room].id_p1) {
            gameStates[ws.room].move_p1 = newMove;
        } else if (ws.uuid === gameStates[ws.room].id_p2) {
            gameStates[ws.room].move_p2 = newMove;
        }
    }
}




function broadcast_game_007(data, room, clients) {
    clients[room].forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            let gameData = JSON.parse(data);
            // Set the "you" and "other" fields based on the player's UUID.
            if (client.uuid === gameData.gameState.id_p1) {
                gameData.gameState.health_you = gameData.gameState.health_p1;
                gameData.gameState.health_other = gameData.gameState.health_p2;
                gameData.gameState.bullets_you = gameData.gameState.bullets_p1;
                gameData.gameState.bullets_other = gameData.gameState.bullets_p2;
                gameData.gameState.move_you = gameData.gameState.move_p1;
                if (gameData.gameState.is_resolving) {
                  gameData.gameState.move_other = gameData.gameState.move_p2;
                  gameData.gameState.videoMove_you = gameData.gameState.move_p1;
                  gameData.gameState.videoMove_other = gameData.gameState.move_p2;
                } else {
                  gameData.gameState.move_other = "!!!";
                  gameData.gameState.videoMove_you = gameData.gameState.videoMove_p1;
                  gameData.gameState.videoMove_other = gameData.gameState.videoMove_p2;
                }
                gameData.gameState.winnerText = gameData.gameState.winnerText_p1;
                gameData.gameState.yourCurrentPrediction = "???";
            } else {
                gameData.gameState.health_you = gameData.gameState.health_p2;
                gameData.gameState.health_other = gameData.gameState.health_p1;
                gameData.gameState.bullets_you = gameData.gameState.bullets_p2;
                gameData.gameState.bullets_other = gameData.gameState.bullets_p1;
                gameData.gameState.move_you = gameData.gameState.move_p2;
                if (gameData.gameState.is_resolving) {
                  gameData.gameState.move_other = gameData.gameState.move_p1;
                  gameData.gameState.videoMove_you = gameData.gameState.move_p2;
                  gameData.gameState.videoMove_other = gameData.gameState.move_p1;
                } else {
                  gameData.gameState.move_other = "!!!";
                  gameData.gameState.videoMove_you = gameData.gameState.videoMove_p2;
                  gameData.gameState.videoMove_other = gameData.gameState.videoMove_p1;
                }
                gameData.gameState.winnerText = gameData.gameState.winnerText_p2;
                gameData.gameState.yourCurrentPrediction = "???";
            }
  
            client.send(JSON.stringify(gameData), {binary: false});
        }
    });
  }
  
  
module.exports = { defaultGameState_007, roundLoop_007, update_007, handleRound_007, broadcast_game_007 }
