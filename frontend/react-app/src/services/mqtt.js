import { connect } from "mqtt";

// const url = "mqtt://10.48.26.128:9001";
// const url = "mqtt://10.48.149.123:9001";
const url = "mqtt://10.48.153.110:9001";
const username = "admin";
const password = "password";

const startMqtt = (tpc, cb) => {
  let counter = 0;
  let client = connect(
    url,
    { username, password }
  );

  client.on("connect", () => {
    client.subscribe(tpc, error => {
      if (error) console.error(error);
    });
  });

  client.on("message", (_topic, message) => {
    cb(`data:image/jpg;base64,${message.toString()}`);
  });
};

export { startMqtt };