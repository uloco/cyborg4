//@flow

import React, { Component } from "react";
import "./App.css";
import { startMqtt } from "./services/mqtt";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: ""
    };
  }
  componentDidMount() {
    startMqtt("cam/stream", url => {
      this.setState({ url });
    });
  }

  render() {
    return (
      <div className="App">
        <img src={this.state.url} />
      </div>
    );
  }
}
export default App;
