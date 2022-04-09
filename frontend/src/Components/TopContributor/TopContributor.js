import React, { Component } from "react";
import "./TopContributor.css";

class TopContributor extends Component {
  render() {
    return (
      <div className={"TopContributor " + this.props.place}>
        <p className="rank"># {this.props.info.rank}</p>
        <img
          className="profile rounded-circle"
          src={this.props.info.image}
          alt={this.props.info.name}
        />
        <p className="name">{this.props.info.name}</p>
        <p className="point">{this.props.info.point} points</p>
      </div>
    );
  }
}

export default TopContributor;
