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

  client.on("message", (topic, message) => {
    if (topic === "state/at_machine") {
      // console.log(message.toString());
    }
    let payload = JSON.stringify([
      {
        name: "State " + Math.random() * 10,
        pnt_lft_up: [100, 100],
        pnt_rght_dwn: [200, 200]
      }
    ]);

    client.publish("state/definition", payload);
    cb(message.toString());
  });
};

export { startMqtt };
