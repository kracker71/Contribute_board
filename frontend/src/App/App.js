import React, { Component } from "react";
import Leaderboard from "../Components/Leaderboard/Leaderboard";
import LeaderboardTitle from "../Components/LeaderboardTitle/LeaderboardTitle";

class App extends Component {
  render() {
    return (
      <div>
        <LeaderboardTitle />
        <Leaderboard />
      </div>
    );
  }
}

export default App;
