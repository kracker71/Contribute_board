import React, { Component } from "react";
import Reward from "../Reward/Reward";

class RewardList extends Component {
  render() {
    const rewardList = this.props.rewardList.map((reward) => {
      return (
        <div className="col">
          <Reward
            key={reward.desc}
            rewardImg={reward.img}
            rewardDesc={reward.desc}
          />
        </div>
      );
    });
    return (
      <div className="RewardList container">
        <div className="row">{rewardList}</div>
      </div>
    );
  }
}

export default RewardList;
