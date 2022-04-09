import React, { Component } from "react";
import "./LeaderboardTitle.css";
import fbLogo from "./fbLogo.png";

class LeaderboardTitle extends Component {
  render() {
    return (
      <div className="LeaderboardTitle">
        <p className="title">Contributor Ranking</p>
        <p className="facebookGroup">
          Poker Thailand Community
          <a
            className="groupLink"
            href="https://www.facebook.com/groups/223422232142743/"
            target="_blank"
            rel="noreferrer"
          >
            <img className="logo" src={fbLogo} alt="fbLogo"></img>
          </a>
        </p>
      </div>
    );
  }
}

export default LeaderboardTitle;
