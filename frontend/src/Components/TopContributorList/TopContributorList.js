import React, { Component } from "react";
import TopContributor from "../TopContributor/TopContributor";

class TopContributorList extends Component {
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <TopContributor info={this.props.contributor[1]} place="second" />
          </div>
          <div className="col">
            <TopContributor info={this.props.contributor[0]} place="first" />
          </div>
          <div className="col">
            <TopContributor info={this.props.contributor[2]} place="third" />
          </div>
        </div>
      </div>
    );
  }
}

export default TopContributorList;
