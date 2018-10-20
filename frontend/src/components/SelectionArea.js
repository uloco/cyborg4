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
    this.ctx = this.refs.canvas.getContext("2d");
  }

  mouseDown(e) {
    e.persist();
    this.point = { name: "State " + this.points.length };
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

    console.log(this.point);
    console.log(this.points);

    if (this.points.length < 3) {
      this.points.push(this.point);
    } else {
      this.points.shift();
      this.points.push(this.point);
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

    // let payload = JSON.stringify([
    //   {
    //     name: "State " + Math.random() * 10,
    //     pnt_lft_up: [this.point.xStart, this.point.yStart],
    //     pnt_rght_dwn: [this.point.xStop, this.point.yStop]
    //   }
    // ]);
    let payload = this.points.map(point => {
      return {
        name: point.name,
        pnt_lft_up: [point.xStart, point.yStart],
        pnt_rght_dwn: [point.xStop, point.yStop]
      };
    });
    console.log("payload", payload);
    this.client.publish("state/definition", JSON.stringify(payload));
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

      let [a, b, c, d] = this.rectangle;
      this.ctx.strokeRect(a, b, c, d);

      this.rectangles.forEach(rectangle => {
        let [a, b, c, d] = rectangle;
        this.ctx.strokeRect(a, b, c, d);
      });
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
