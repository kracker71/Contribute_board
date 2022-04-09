import React, { Component } from "react";
import Contributor from "../Contributor/Contributor.js";

class ContributorList extends Component {
  render() {
    const contributorList = this.props.contributor.map((contributor) => {
      return <Contributor info={contributor} />;
    });
    return (
      <div className="table-responsive">
        <table className="table table-light align-middle">
          <thead className="table-dark">
            <tr>
              <th className="col-1">#</th>
              <th className="col-1">Profile</th>
              <th className="col-8">Name</th>
              <th className="col-2">Points</th>
            </tr>
          </thead>
          <tbody>{contributorList}</tbody>
        </table>
      </div>
    );
  }
}

export default ContributorList;
