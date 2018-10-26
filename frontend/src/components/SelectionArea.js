import React, { Component } from "react";

import { connect } from "mqtt";
import { url } from "../services/mqtt";

const username = "admin";
const password = "password";

/**
 * Class selection area
 */
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
    this.client.publish("state/definition", JSON.stringify({ points: [] }));
  }

  clearRects() {
    this.point = {};
    this.points = [];
    this.rectangle = {};
    this.rectangles = [];
    this.ctx.clearRect(0, 0, this.refs.canvas.width, this.refs.canvas.height);
    this.client.publish("state/definition", JSON.stringify({ points: [] }));
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
    console.debug("points", this.points);
    console.debug("rectangles", this.rectangles);

    let payload = {
      points: this.points.map(point => {
        return {
          name: point.name,
          pnt_lft_up: [point.xStart, point.yStart],
          pnt_rght_dwn: [point.xStop, point.yStop]
        };
      })
    };
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
    return this.rectangles.forEach(rect => this.draw(rect));
  }

  draw(rect) {
    console.log(rect);
    return this.ctx.strokeRect.apply(this, rect);
  }

  render() {
    return (
      <canvas
        ref="canvas"
        id="canvas"
        width="500"
        height="281"
        onMouseDown={this.mouseDown}
        onMouseUp={this.mouseUp}
        onMouseMove={this.mouseMove}
      />
    );
  }
}
