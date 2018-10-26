import { connect } from "mqtt";

export const url = "mqtt://10.192.254.241:9001";
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
