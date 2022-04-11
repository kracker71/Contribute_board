import React, { Component } from "react";
import Leaderboard from "../Components/Leaderboard/Leaderboard";
import LeaderboardTitle from "../Components/LeaderboardTitle/LeaderboardTitle";
import RewardModal from "../Components/RewardModal/RewardModal";
import RewardList from "../Components/RewardList/RewardList";
import RewardTitle from "../Components/RewardTitle/RewardTitle";

class App extends Component {
  render() {
    return (
      <div>
        <RewardTitle />
        <RewardList />
        <RewardModal />
        <LeaderboardTitle />
        <Leaderboard />
      </div>
    );
  }
}

export default App;
