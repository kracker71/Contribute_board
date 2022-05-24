import React, { Component } from "react";
import "./TopContributorList.css";
import TopContributor from "../TopContributor/TopContributor";

class TopContributorList extends Component {
  render() {
    return (
      <div className="TopContributorList container">
        <div className="row">
          <div className="col col-second">
            <TopContributor info={this.props.contributor[1]} place="second" />
          </div>
          <div className="col col-first">
            <TopContributor info={this.props.contributor[0]} place="first" />
          </div>
          <div className="col col-third">
            <TopContributor info={this.props.contributor[2]} place="third" />
          </div>
        </div>
      </div>
    );
  }
}

export default TopContributorList;
