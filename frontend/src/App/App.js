import React, { Component } from "react";
import "./App.css";
import Leaderboard from "../Components/Leaderboard/Leaderboard";
import LeaderboardTitle from "../Components/LeaderboardTitle/LeaderboardTitle";
import NavigationBar from "../Components/NavigationBar/NavigationBar";

class App extends Component {
  render() {
    return (
      <div>
        <div className="background">
          <div className="background-filter">
            {/* <NavigationBar /> */}
            <LeaderboardTitle />
            {/* <Leaderboard /> */}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
