# HandLand

Welcome to HandLand! A platform to create live AI multiplayer games using WebRTC, Websockets, and Roboflow for AI vision models.

## Live Demo

[HandLand.lol](https://handland.lol)

## Features

- **Backend**: Simple Express JS server
- **Multiplayer**: WebRTC and native Websockets
- **AI Vision**: Integrated with Roboflow (sponsored project)

## Getting Started

This is a template for making silly multiplayer games that involve your hands and body. You can submit new games to the repo and I will host them.

The files are very short so you can mess around with them and make new games or just learn how websockets work. It has the most basic matchmaking possible as well as a shareable links - whoever has the same link as you will be in your "room".

HandLand can be uploaded as is to popular cloud platforms like Vercel or Heroku.

### Prerequisites

1. Get a free API key from [Roboflow](https://roboflow.com/) to use their vision models.
2. Paste into each game main.js file here 
```
var publishable_key = "YOUR_ROBOFLOW_KEY_HERE";
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/yourusername/HandLand.git
   cd HandLand
   ```
2. Install dependencies
   ```sh
   npm install
   ```
3. Start the server
   ```sh
   npm start
   ```

## Included Games

HandLand comes with three complete two-player games:

1. **Rock, Paper, Scissors**
2. **Staring Contest**
3. **007 (Standoff or Block, Reload, Shoot, and Shotgun)**
   - [How to play](https://www.wikihow.com/Play-the-Shotgun-Game)

## Deployment

### Vercel

1. [Sign up](https://vercel.com/signup) or log in to Vercel.
2. Create a new project from the Vercel dashboard.
3. Connect your GitHub repository.
4. Click "Deploy".


### Heroku

1. [Sign up](https://signup.heroku.com) or log in to Heroku.
2. Create a new app from the Heroku dashboard.
3. Connect your GitHub repository.
4. Click "Deploy Branch".

## Acknowledgements

- Thanks to Roboflow for sponsoring this project. Get your free API key at: [Roboflow](https://roboflow.com/)

## License

Distributed under the APACHE 2.0 License. See `LICENSE` for more information.

## Contact

Twitter: [@j_stonemountain](https://twitter.com/j_stonemountain)

Youtube: [How to Video coming soon](https://www.youtube.com/@mr.stonemountain)

Project Link: [https://github.com/jamespsteinberg/handland](https://github.com/jamespsteinberg/handland)
