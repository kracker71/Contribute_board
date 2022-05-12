import React, { Component } from "react";
import "./ContributorList.css";
import Contributor from "../Contributor/Contributor.js";
import { Container, Row, Col } from "react-bootstrap";

class ContributorList extends Component {
  render() {
    const contributorList = this.props.contributor.map((contributor) => {
      return <Contributor info={contributor} />;
    });
    return (
      <div className="ContributorList">
        <Container>{contributorList}</Container>
      </div>
    );
  }
}

export default ContributorList;
