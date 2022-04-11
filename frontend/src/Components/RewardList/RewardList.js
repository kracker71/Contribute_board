import React, { Component } from "react";
import Reward from "../Reward/Reward";
import rewardImg from "./reward.png";

const rewardList = [];

for (let i = 1; i <= 3; i++) {
  const rewardInfo = {
    img: rewardImg,
    desc: `ของรางวัล ${i}`,
  };
  rewardList.push(rewardInfo);
}

class RewardList extends Component {
  render() {
    return rewardList.map((reward) => {
      return (
        <Reward
          key={reward.desc}
          rewardImg={reward.img}
          rewardDesc={reward.desc}
        />
      );
    });
  }
}

export default RewardList;
