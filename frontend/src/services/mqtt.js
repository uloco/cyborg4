import { connect } from "mqtt";

// const url = "mqtt://10.48.26.128:9001";
// const url = "mqtt://10.48.149.123:9001";
const url = "mqtt://10.48.153.110:9001";
const username = "admin";
const password = "password";

const startMqtt = (tpc, cb) => {
  let client = connect(
    url,
    { username, password }
  );

  client.on("connect", () => {
    client.subscribe(tpc, error => {
      if (error) console.error(error);
    });
  });

  client.on("message", (topic, message) => {
    if (topic === "state/at_machine") {
      // console.log(message.toString());
    }

    // client.publish("state/definition", payload);
    cb(message.toString());
  });
};

export { startMqtt };
