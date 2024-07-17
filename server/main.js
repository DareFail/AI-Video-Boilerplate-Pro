'use strict';

const express = require('express');
const WebSocket = require('ws');
const http = require('http');
const path = require('path');
const { defaultGameState_staring, handleRound_staring, roundLoop_staring  } = require('../games/staring/server.js');
const { defaultGameState_rps, update_rps, roundLoop_rps } = require('../games/rps/server.js');
const { defaultGameState_007, update_007, roundLoop_007 } = require('../games/007/server.js');
const PORT = process.env.PORT || 3000;

const app = express();

// Serve static files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname,'../home/index.html'));
});

app.get('/index.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../home/index.js'));
});

app.get('/common.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../common/common.js'));
});

app.get('/common.css', (req, res) => {
  res.sendFile(path.join(__dirname,'../common/common.css'));
});

app.get('/annotation.png', (req, res) => {
  res.sendFile(path.join(__dirname,'../media/annotation.png'));
});

app.get('/demo.webp', (req, res) => {
  res.sendFile(path.join(__dirname,'../media/demo.webp'));
});

app.get('/frames.png', (req, res) => {
  res.sendFile(path.join(__dirname,'../media/frames.png'));
});




app.get('/staring/main.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/staring/main.js'));
});

app.get('/staring/game.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/staring/game.js'));
});

app.get('/staring/*', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/staring/staring.html'));
});


app.get('/rps/main.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/rps/main.js'));
});

app.get('/rps/game.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/rps/game.js'));
});

app.get('/rps/*', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/rps/rps.html'));
});


app.get('/007/main.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/007/main.js'));
});

app.get('/007/game.js', (req, res) => {
  res.sendFile(path.join(__dirname,'../games/007/game.js'));
});

app.get('/007/*', (req, res) => {
    res.sendFile(path.join(__dirname,'../games/007/007.html'));
});



const server = http.createServer(app);

server.listen(PORT, () => console.log(`HTTP Server running on port ${PORT}`));

// Initialize Websocket server
const wss = new WebSocket.Server({ server });

// Store clients in rooms based on url
let clients = {};
let gameStates = {}; 


wss.on('connection', (ws, req) => {

  ws.on('message', message => {
    let parsedMessage = JSON.parse(message);
    if (parsedMessage.command === 'connect') { 
      ws.uuid = parsedMessage.uuid; 
      ws.room = parsedMessage.room;
      const game = parsedMessage.room.split("/")[1];

      if (!clients[ws.room]) {
        clients[ws.room] = [];
      }
    
      if (clients[ws.room].length >= 2) {
        ws.send("Room is full");
        ws.close();
        return;
      }
      
      clients[ws.room].push(ws);

      if (game === 'staring') {
        gameStates[ws.room] = { ...defaultGameState_staring };

        if (clients[ws.room].length === 2) {

          gameStates[ws.room].id_p1 = clients[ws.room][0].uuid;
          gameStates[ws.room].id_p2 = clients[ws.room][1].uuid;
          
          roundLoop_staring(gameStates, ws, clients);
        }
      } else if (game === 'rps') {
        gameStates[ws.room] = { ...defaultGameState_rps };

        if (clients[ws.room].length === 2) {

          gameStates[ws.room].id_p1 = clients[ws.room][0].uuid;
          gameStates[ws.room].id_p2 = clients[ws.room][1].uuid;

          roundLoop_rps(gameStates, ws, clients);
        }
      } else if (game === '007') {
        gameStates[ws.room] = { ...defaultGameState_007 };

        if (clients[ws.room].length === 2) {

          gameStates[ws.room].id_p1 = clients[ws.room][0].uuid;
          gameStates[ws.room].id_p2 = clients[ws.room][1].uuid;
          
          roundLoop_007(gameStates, ws, clients);
        }
      }
    
      console.log(`Client ${ws.uuid} connected to room ${ws.room}`);

    } else if (parsedMessage.command === 'getOldestRoomWithOnePerson') {
      const room = getOldestRoomWithOnePerson(ws.room);
      if (room) {
          ws.send(JSON.stringify({room: room}))
      } else {
          ws.send('All rooms are empty :(')
      }
    } else if (parsedMessage.command === "updateGameState") {
      const game = ws.room.split("/")[1];
      if (game == "staring" && gameStates[ws.room].is_playing) {
        //console.log(`Received: ${message}`);
        handleRound_staring(gameStates, parsedMessage.action, ws, clients);
      } else if (game == "rps") {
        //console.log(`Received: ${message}`);
        update_rps(gameStates, parsedMessage.action, ws);
      } else if (game == "007") {
        //console.log(`Received: ${message}`);
        update_007(gameStates, parsedMessage.action, ws);
      }
    } else {
      //console.log(`Received: ${message}`);
      broadcast_video(message, ws.room, ws);
    }

  });

  ws.on('error', err => console.log(`Server error: ${err}`));

  ws.on('close', () => {
    clients[ws.room] = clients[ws.room].filter(client => client !== ws);
  });
});

function broadcast_video(data, room, exclude) {
  clients[room].forEach(client => {
    if (client !== exclude && client.readyState === WebSocket.OPEN) {
      client.send(data, {binary: false});
    }
  });
}



function getOldestRoomWithOnePerson(excludedRoom) {
  for (let room in clients) {
      if (clients[room].length === 1 && room !== excludedRoom) {
          return room;
      }
  }
  return null;
}

wss.on('error', err => console.log(`Server error: ${err}`));
