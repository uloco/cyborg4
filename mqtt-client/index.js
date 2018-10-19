var mqtt = require('mqtt')
var client  = mqtt.connect('mqtt://localhost')

client.on('connect', function () {
  subscribe();
});

client.on('message', function (topic, message) {
  // message is Buffer
  console.log('Topic: ', topic, 'Message:', message.toString())
});

function subscribe() {
  client.subscribe('cam/stream', function (err) {
    if (err) {
      console.error(err);
    }
  });
}