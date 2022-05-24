import React, { Component } from "react";
import "./TopContributor.css";
import crownImg from "./crown.png";

class TopContributor extends Component {
  render() {
    return (
      <div className={"TopContributor " + this.props.place}>
        <div className="profile-group">
          <img className="crown" src={crownImg} alt="crown" />
          <img
            className="profile"
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
        </div>
        <div className="name">{this.props.info.name}</div>
        <div className="point">{this.props.info.point}</div>
      </div>
    );
  }
}

export default TopContributor;
