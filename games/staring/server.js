'use strict';
const WebSocket = require('ws');

const defaultGameState_staring = {
  id_p1: "",
  id_p2: "",
  health_p1: 3,
  health_p2: 3,
  move_p1: '',
  move_p2: '',
  videoMove_p1: "",
  videoMove_p2: "",
  end_game: false,
  is_playing: false,
  remoteVideoVisible: false,
  gameStateText: "",
  winnerText_p1: "",
  winnerText_p2: ""
}


function handleRound_staring(gameStates, newMove, ws, clients) {
  if (gameStates[ws.room].is_playing) {
      if (newMove == "Keep Eyes Open!") {
        if (ws.uuid === gameStates[ws.room].id_p1) {
          gameStates[ws.room].move_p1 = "UH OH!";
          gameStates[ws.room].videoMove_p1 = "Keep Eyes Open!";
        } else if (ws.uuid === gameStates[ws.room].id_p2) {
            gameStates[ws.room].move_p2 = "UH OH!"
            gameStates[ws.room].videoMove_p2 = "Keep Eyes Open!";
        }
        broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
      }
      if (newMove == "Blinking") {
          if (ws.uuid === gameStates[ws.room].id_p1) {
              gameStates[ws.room].health_p1 = gameStates[ws.room].health_p1 - 1;
              gameStates[ws.room].move_p1 = "BLINK!";
              gameStates[ws.room].videoMove_p1 = "BLINK!";
          } else if (ws.uuid === gameStates[ws.room].id_p2) {
              gameStates[ws.room].health_p2 = gameStates[ws.room].health_p2 - 1;
              gameStates[ws.room].move_p2 = "BLINK!"
              gameStates[ws.room].videoMove_p2 = "BLINK!";
          }
          gameStates[ws.room].is_playing = false;
          
          if (gameStates[ws.room].health_p1 <= 0 || gameStates[ws.room].health_p2 <= 0) {
              gameStates[ws.room].end_game = true;
              if (health_p2 <= 0) {
                gameStates[ws.room].winnerText_p1 = "WINNER!"
                gameStates[ws.room].winnerText_p2 = "DEFEAT!"
              } else {
                gameStates[ws.room].winnerText_p1 = "DEFEAT!"
                gameStates[ws.room].winnerText_p2 = "WINNER!"
              }
              broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);

          } else {
            roundLoop_staring(gameStates, ws, clients);

          }
          
      }
  }
}



function roundLoop_staring(gameStates, ws, clients) {
  gameStates[ws.room].remoteVideoVisible = false;
    broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
    setTimeout(() => {
      gameStates[ws.room].gameStateText = "1";
      broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
      setTimeout(() => {
        gameStates[ws.room].gameStateText = "1, 2";
        gameStates[ws.room].videoMove_p1 = "";
        gameStates[ws.room].videoMove_p2 = "";
        broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
        setTimeout(() => {
          gameStates[ws.room].gameStateText = "1, 2, Go!";
          broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
          setTimeout(() => {  
            gameStates[ws.room].remoteVideoVisible = true;
            gameStates[ws.room].gameStateText = "";
            gameStates[ws.room].is_playing = true;
            broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
          }, 1000);
          broadcast_game_staring(JSON.stringify({ gameState: gameStates[ws.room] }), ws.room, clients);
        }, 2000);
      }, 2000);
    }, 2000);
}


function broadcast_game_staring(data, room, clients) {
  clients[room].forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
          let gameData = JSON.parse(data);
          // Set the "you" and "other" fields based on the player's UUID.
          if (client.uuid === gameData.gameState.id_p1) {
              gameData.gameState.health_you = gameData.gameState.health_p1;
              gameData.gameState.health_other = gameData.gameState.health_p2;
              gameData.gameState.move_you = gameData.gameState.move_p1;
              gameData.gameState.move_other = gameData.gameState.move_p2;
              gameData.gameState.videoMove_you = gameData.gameState.videoMove_p1;
              gameData.gameState.videoMove_other = gameData.gameState.videoMove_p2;
              if (gameData.gameState.videoMove_other == "BLINK!") {
                gameData.gameState.videoMove_other = "THEY BLUNK!"
                ameData.gameState.videoMove_you = "";
              } else if (gameData.gameState.videoMove_other == "Keep Eyes Open!") {
                gameData.gameState.videoMove_other = "WIDER EYES!";
              }
              gameData.gameState.winnerText = gameData.gameState.winnerText_p1;
              
          } else {
              gameData.gameState.health_you = gameData.gameState.health_p2;
              gameData.gameState.health_other = gameData.gameState.health_p1;
              gameData.gameState.move_you = gameData.gameState.move_p2;
              gameData.gameState.move_other = gameData.gameState.move_p1;
              gameData.gameState.videoMove_you = gameData.gameState.videoMove_p2;
              gameData.gameState.videoMove_other = gameData.gameState.videoMove_p1;
              if (gameData.gameState.videoMove_other == "BLINK!") {
                gameData.gameState.videoMove_other = "THEY BLUNK!"
                ameData.gameState.videoMove_you = "";
              } else if (gameData.gameState.videoMove_other == "Keep Eyes Open!") {
                gameData.gameState.videoMove_other = "WIDER EYES!";
              }
              gameData.gameState.winnerText = gameData.gameState.winnerText_p2;
          }
          client.send(JSON.stringify(gameData), {binary: false});
      }
  });
}


module.exports = { defaultGameState_staring, handleRound_staring, broadcast_game_staring, roundLoop_staring }
