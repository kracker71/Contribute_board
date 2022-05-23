import React, { Component } from "react";
import "./ContributorList.css";
import Contributor from "../Contributor/Contributor.js";
import { Container } from "react-bootstrap";

class ContributorList extends Component {
  render() {
    const contributorList = this.props.contributor.map((contributor) => {
      return <Contributor info={contributor} key={contributor.rank} />;
    });
    return (
      <div className="ContributorList">
        <Container>{contributorList}</Container>
      </div>
    );
  }
}

export default ContributorList;
