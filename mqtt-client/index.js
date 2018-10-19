var mqtt = require('mqtt')
var client  = mqtt.connect('mqtt://10.48.155.253')

client.on('connect', function () {
  subscribe();
});

client.on('message', function (topic, message) {
  // message is Buffer
  console.log('Topic: ', topic, 'Message:', message.toString())
});

function subscribe() {
  client.subscribe('machine/data/state', function (err) {
    if (err) {
      console.error(err);
    }
  });
}