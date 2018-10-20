//@flow

import React, { Component } from "react";
import "./App.css";
import { startMqtt } from "./services/mqtt";
import SelectionArea from "./components/SelectionArea";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      machineState: "",
      timestamp: 0
    };
  }
  componentDidMount() {
    startMqtt("cam/stream", url => {
      this.setState({
        ...this.state,
        url: `data:image/jpg;base64,${url}`
      });
    });
    startMqtt("state/at_machine", machineState => {
      let { state, timestamp } = JSON.parse(machineState).state_data;
      timestamp = new Date(timestamp).toLocaleString("de-DE");
      this.setState({
        ...this.state,
        machineState: state,
        timestamp: timestamp
      });
    });
  }

  render() {
    return (
      <div className="App">
        <SelectionArea />
        <img src={this.state.url} alt="foo" />
        <p>Current State</p>
        <p>{this.state.machineState}</p>
        <p>{this.state.timestamp}</p>
      </div>
    );
  }
}
export default App;
