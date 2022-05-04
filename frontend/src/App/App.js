import React, { Component } from "react";
import Leaderboard from "../Components/Leaderboard/Leaderboard";
import LeaderboardTitle from "../Components/LeaderboardTitle/LeaderboardTitle";
import NavigationBar from "../Components/NavigationBar/NavigationBar";

class App extends Component {
  render() {
    return (
      <div>
        {/* <NavigationBar /> */}
        <LeaderboardTitle />
        {/* <Leaderboard /> */}
      </div>
    );
  }
}

export default App;
