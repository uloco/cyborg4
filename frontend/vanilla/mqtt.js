let client = mqtt.connect("mqtt://10.48.149.123:9001");

client.on("connect", function() {
  client.subscribe("presence", function(err) {
    if (!err) {
      client.publish("presence", "Hello mqtt");
    }
  });
});

client.on("message", function(topic, message) {
  // message is Buffer
  console.log(message.toString());
  client.end();
});
