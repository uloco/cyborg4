import React, { Component } from "react";

export default class SelectionArea extends Component {
  constructor(props) {
    super(props);
    this.mouseUp = this.mouseUp.bind(this);
    this.mouseDown = this.mouseDown.bind(this);
    this.mouseMove = this.mouseMove.bind(this);
    this.state = {
      drag: false,
      rectangles: [],
      point: {},
      points: []
    };
  }

  componentDidMount() {
    // this.setState({
    //   ctx: this.refs.canvas.getContext("2d")
    // });
  }

  mouseDown(e) {
    e.persist();
    let { left, top } = this.refs.canvas.getBoundingClientRect();
    this.setState({
      point: { xStart: e.clientX - left, yStart: e.clientY - top },
      drag: true
    });
    // this.state.point.xStart = e.clientX - left;
    // this.state.point.yStart = e.clientY - top;
  }

  mouseUp(e) {
    e.persist();
    let { left, top } = this.refs.canvas.getBoundingClientRect();
    this.setState({
      point: { xStop: e.clientX - left, yStop: e.clientY - top },
      drag: false
    });
    // this.state.point.xStop = e.clientX - left;
    // this.state.point.yStop = e.clientY - top;
    // this.drag = false;

    if (this.state.points.length <= 1) {
      this.setState({
        points: [...this.state.points, this.state.point]
      });
    } else {
      let points = [...this.state.points];
      points.shift();
      points.push(this.state.point);
      this.setState({
        points
      });
    }
  }

  mouseMove(e) {
    e.persist();
    if (this.state.drag) {
      this.ctx = this.refs.canvas.getContext("2d");
      let { left, top } = this.refs.canvas.getBoundingClientRect();
      this.ctx.clearRect(0, 0, this.refs.canvas.width, this.refs.canvas.height);
      this.ctx.strokeStyle = "#FF0000";
      this.ctx.strokeRect(
        this.state.point.xStart,
        this.state.point.yStart,
        e.clientX - left - this.state.point.xStart,
        e.clientY - top - this.state.point.yStart
      );
    }
  }

  render() {
    return (
      <canvas
        ref="canvas"
        id="canvas"
        width="500"
        height="320"
        onMouseDown={this.mouseDown}
        onMouseUp={this.mouseUp}
        onMouseMove={this.mouseMove}
      />
    );
  }
}
