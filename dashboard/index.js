/* jshint esversion: 6, module: true, browser: true, devel: true */
/* globals Vue */

const hostname = window.location.hostname;
const default_listener_url = 'ws://' + hostname + ':5678';

// Websocket connection to the Penny joystick listener server.
let gamepad_listener_socket;

// UI state
let ui_state = {
  'gamepads': {},
  'connection': {
    'connected': false
  }
};

/* Gamepad updates */
function prepareGamepadData() {
  let gamepads = navigator.getGamepads();
  
  let gamepad_data = {};
  for(let n = 0; n < gamepads.length; n++) {
    let gamepad = gamepads[n];
    if (gamepad == null) {
      continue;
    }

    let buttons = {};
    for(n in gamepad.buttons) {
      buttons[n] = gamepad.buttons[n].pressed;
    }

    gamepad_data[gamepad.index] = {
      'axes': gamepad.axes,
      'buttons': buttons
    };
  }

  return gamepad_data;
}


/* Communication with server */
function establishConnection(url) {
  url = url || default_listener_url;
  let send_data_interval;
  
  ui_state.connection.connected = false;
  ui_state.connection.error = null;

  gamepad_listener_socket = new WebSocket(url);

  gamepad_listener_socket.onerror = (e) => {
    if(send_data_interval) {
      window.clearInterval(send_data_interval);
    }
    ui_state.connection.connected = false;
  };

  gamepad_listener_socket.onclose = (e) => {
    if(send_data_interval) {
      window.clearInterval(send_data_interval);
    }
    ui_state.connection.connected = false;
    if(e.code == 1000) return;
    ui_state.connection.error = e.code + ': ' + e.reason;
  };

  gamepad_listener_socket.onopen = (e) => {
    ui_state.connection.connected = true;
    // send data at 30hz
    send_data_interval = window.setInterval(
      sendGamepadDataToServer, 1000 / 30);
  };
}

function sendGamepadDataToServer() {
  let data = prepareGamepadData();
  gamepad_listener_socket.send(JSON.stringify(data));
}

/* UI */
let app = new Vue({
  el: '#app',
  data: ui_state,
  methods: {
    connect: () => {
      establishConnection(default_listener_url);
    }
  }
});

function updateGamepadUI() {
  ui_state.gamepads = prepareGamepadData();
}

window.setInterval(updateGamepadUI, 100);
