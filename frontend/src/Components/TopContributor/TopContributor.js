import React, { Component } from "react";
import "./TopContributor.css";

class TopContributor extends Component {
  render() {
    return (
      <div className={"TopContributor " + this.props.place}>
        <img
          className="profile rounded-circle"
          src={this.props.info.image}
          alt={this.props.info.name}
        />
        <div className="rank-spade">
          <div className="spade">
            <div className="shape">
              <span className="heart">
                <span className="tale"></span>
              </span>
            </div>
          </div>
        </div>
        <div className="rank">{this.props.info.rank}</div>
        <div className="name">{this.props.info.name}</div>
        <div className="point">{this.props.info.point}</div>
      </div>
    );
  }
}

export default TopContributor;
