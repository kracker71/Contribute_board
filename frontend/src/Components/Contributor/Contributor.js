import React, { Component } from "react";
import "./Contributor.css";

class Contributor extends Component {
  render() {
    return (
      <tr className="Contributor">
        <th className="rank" scope="row">
          {this.props.info.rank}
        </th>
        <td>
          <img
            className="profile"
            src={this.props.info.image}
            alt={this.props.info.name}
          />
        </td>
        <td className="name">{this.props.info.name}</td>
        <td className="point">{this.props.info.point}</td>
      </tr>
    );
  }
}

export default Contributor;
