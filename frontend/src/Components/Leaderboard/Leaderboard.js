import React, { Component } from "react";
import ContributorList from "../ContributorList/ContributorList";
import TopContributorList from "../TopContributorList/TopContributorList";
import profileImg from "./profile_img.jpg";

const allContributorList = [];

for (let i = 1; i <= 10; i++) {
  allContributorList.push({
    rank: i,
    image: profileImg,
    name: "Chavalvit Keartnattakorn",
    point: 20000,
  });
}

const topContributorList = allContributorList.slice(0, 3);
const contributorList = allContributorList.slice(3);

class Leaderboard extends Component {
  render() {
    return (
      <div>
        <TopContributorList contributor={topContributorList} />
        <ContributorList contributor={contributorList} />
      </div>
    );
  }
}

export default Leaderboard;
