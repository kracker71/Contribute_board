import React, { Component } from "react";
import "./Contributor.css";
import { Row, Col } from "react-bootstrap";

class Contributor extends Component {
  render() {
    return (
      <div className="Contributor">
        <Row xs={4}>
          <Col className="rank" xs={1} sm={1}>
            {this.props.info.rank}
          </Col>
          <Col className="profile" xs={1} sm={1}>
            <img
              className="rounded-circle"
              src={this.props.info.image}
              alt={this.props.info.image}
            />
          </Col>
          <Col className="name" xs={8} sm={8}>
            {this.props.info.name}
          </Col>
          <Col className="point" xs={2} sm={2}>
            {this.props.info.point}
          </Col>
        </Row>
      </div>
    );
  }
}

export default Contributor;
