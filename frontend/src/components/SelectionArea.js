import React, { Component } from "react";
import { startMqtt } from "../services/mqtt";

import { connect } from "mqtt";

const url = "mqtt://10.48.153.110:9001";
const username = "admin";
const password = "password";

export default class SelectionArea extends Component {
  constructor(props) {
    super(props);
    this.mouseUp = this.mouseUp.bind(this);
    this.mouseDown = this.mouseDown.bind(this);
    this.mouseMove = this.mouseMove.bind(this);
  }
  componentDidMount() {
    this.drag = false;
    this.rectangle = {};
    this.rectangles = [];
    this.point = {};
    this.points = [];
    this.client = connect(
      url,
      { username, password }
    );
  }

  mouseDown(e) {
    e.persist();
    let { left, top } = this.refs.canvas.getBoundingClientRect();
    this.point.xStart = e.clientX - left;
    this.point.yStart = e.clientY - top;
    this.drag = true;
  }

  mouseUp(e) {
    e.persist();
    let { left, top } = this.refs.canvas.getBoundingClientRect();
    this.point.xStop = e.clientX - left;
    this.point.yStop = e.clientY - top;
    this.drag = false;

    if (this.points.length < 2) {
      this.points = [...this.points, this.point];
    } else {
      let points = [...this.points];
      points.shift();
      points.push(this.point);
      this.points = points;
    }

    if (this.rectangles.length < 2) {
      this.rectangles.push([
        this.point.xStart,
        this.point.yStart,
        e.clientX - left - this.point.xStart,
        e.clientY - top - this.point.yStart
      ]);
    } else {
      this.rectangles.shift();
      this.rectangles.push([
        this.point.xStart,
        this.point.yStart,
        e.clientX - left - this.point.xStart,
        e.clientY - top - this.point.yStart
      ]);
    }
    console.log("points", this.points);
    console.log("rectangles", this.rectangles);
    let payload = JSON.stringify([
      {
        name: "State " + Math.random() * 10,
        pnt_lft_up: [this.point.xStart, this.point.yStart],
        pnt_rght_dwn: [this.point.xStop, this.point.yStop]
      }
    ]);

    console.log(payload);
    this.client.publish("state/definition", payload);
  }

  mouseMove(e) {
    e.persist();
    if (this.drag) {
      this.ctx = this.refs.canvas.getContext("2d");
      let { left, top } = this.refs.canvas.getBoundingClientRect();
      this.ctx.clearRect(0, 0, this.refs.canvas.width, this.refs.canvas.height);
      this.ctx.strokeStyle = "#FF0000";
      this.rectangle = [
        this.point.xStart,
        this.point.yStart,
        e.clientX - left - this.point.xStart,
        e.clientY - top - this.point.yStart
      ];

      this.ctx.strokeRect(
        this.point.xStart,
        this.point.yStart,
        e.clientX - left - this.point.xStart,
        e.clientY - top - this.point.yStart
      );
      // this.rectangles.forEach(args => {
      //   if (args && Array.isArray(args)) {
      //     console.log(args);
      //     // this.ctx.strokeRect.apply(null, args);
      //   }
      // });
    }
  }

  drawRects(e) {
    return this.rectangles.forEach(args => this.draw(args));
  }

  draw(args) {
    console.log(args);
    return this.ctx.strokeRect.apply(this, args);
  }

  render() {
    return (
      <canvas
        ref="canvas"
        id="canvas"
        width="500"
        height="375"
        onMouseDown={this.mouseDown}
        onMouseUp={this.mouseUp}
        onMouseMove={this.mouseMove}
      />
    );
  }
}
