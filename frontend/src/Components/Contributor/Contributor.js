import React, { Component } from "react";
import "./Contributor.css";
import { Row, Col } from "react-bootstrap";

class Contributor extends Component {
  render() {
    return (
      <div className="Contributor">
        <Row lg={4}>
          <Col className="rank" lg={1}>
            {this.props.info.rank}
          </Col>
          <Col className="profile" lg={1}>
            <img
              className="rounded-circle"
              src={this.props.info.image}
              alt={this.props.info.image}
            />
          </Col>
          <Col className="name" lg={8}>
            {this.props.info.name}
          </Col>
          <Col className="point" lg={2}>
            {this.props.info.point}
          </Col>
        </Row>
      </div>
    );
  }
}

export default Contributor;
