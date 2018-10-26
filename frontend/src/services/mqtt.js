import { connect } from "mqtt";

export const url = "mqtt://10.192.254.71:9001";
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
    cb(message);
    client.unsubscribe(topic, () => client.subscribe(topic, error => { if (error) console.error(error) }));
  });
};

export { startMqtt };
