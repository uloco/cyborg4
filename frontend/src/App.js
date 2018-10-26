//@flow

import React, { Component } from "react";
import "./App.css";
import { startMqtt } from "./services/mqtt";
import SelectionArea from "./components/SelectionArea";

class App extends Component {

  dateOptions = { year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric' };

  historyItems;

  constructor(props) {
    super(props);
    this.state = {
      url: "",
      machineState: "-",
      timestamp: 0,
      history: []
    };
    this.resetSelection = this.resetSelection.bind(this);
    this.selectionAreaComponent = React.createRef();
  }

  componentDidMount() {

    // Start camera stream
    startMqtt("cam/stream", url => {
      this.setState({
        ...this.state,
        url: `data:image/jpg;base64,${url}`
      });
    });

    // Start machine state
    startMqtt("state/at_machine", machineState => {
      let { state, timestamp } = JSON.parse(machineState).state_data;
      timestamp = new Date(timestamp).toLocaleString("de-DE", this.dateOptions);



      if (this.state.history.length === 20) {
        this.state.history.splice(0, 1);
      }
      this.state.history.push({
        machineState: state,
        timestamp: timestamp
      });


      this.historyItems = this.state.history.map((state) =>
        <tr>
          <td>{state.machineState}</td>
          <td>{state.timestamp}</td>
        </tr>);

      this.setState({
        ...this.state,
        machineState: state,
        timestamp: timestamp
      });
    });

  }

  resetSelection(event) {
    this.selectionAreaComponent.current.clearRects();
  }

  render() {
    return (
      <div className="App">
        <h3>Easy Production Streamer</h3>
        <div className="wrapper">
          <div className="column">
            <div className="stream-area">
              <SelectionArea ref={this.selectionAreaComponent} />
              <img src={this.state.url} alt="View stream." />
              <div className="button-area">
                <button className="reset-button" onClick={this.resetSelection}>Reset selection</button>
              </div>
            </div>
            <h4>Current State</h4>
            <div className="table">
              <div className="row">
                <div>Machine state:</div><div>{this.state.machineState}</div>
              </div>
              <div className="row">
                <div>Timestamp:</div><div>{this.state.timestamp}</div>
              </div>
            </div>
          </div>
          <div className="column">
            <table>
              <tbody>
                <tr>
                  <th>State</th>
                  <th>TimeStamp</th>
                </tr>
                {this.historyItems}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}
export default App;
