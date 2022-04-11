import React, { Component } from "react";
import "./Reward.css";

class Reward extends Component {
  render() {
    return (
      <div className="Reward">
        <img className="rewardImg" src={this.props.rewardImg} alt="rewardImg" />
        <p className="rewardDesc">{this.props.rewardDesc}</p>
      </div>
    );
  }
}

export default Reward;
