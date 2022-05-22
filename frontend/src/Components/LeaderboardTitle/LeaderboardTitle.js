import React, { Component } from "react";
import "./LeaderboardTitle.css";
import fbLogo from "./fbLogo.png";

class LeaderboardTitle extends Component {
  render() {
    return (
      <div className="LeaderboardTitle">
        <p className="facebook-group">
          โป๊กเกอร์ Thailand
          <a
            className="groupLink"
            href="https://www.facebook.com/groups/291396973145616"
            target="_blank"
            rel="noreferrer"
          >
            <img className="logo" src={fbLogo} alt="facebook-logo"></img>
          </a>
        </p>
        <p className="title">Contributor Ranking</p>
        <p className="sub-title">ตารางจัดอันดับผู้มีส่วนร่วมในกลุ่ม</p>
      </div>
    );
  }
}

export default LeaderboardTitle;
