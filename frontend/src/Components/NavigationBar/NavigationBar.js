import React, { Component } from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import "./NavigationBar.css";
import RewardModal from "../RewardModal/RewardModal";

class NavigationBar extends Component {
  render() {
    return (
      <Navbar expand="md" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand bsPrefix="navbar-brand" href="#home">
            โป๊กเกอร์ Thailand
          </Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse>
            <Nav className="me-auto">
              <Nav.Link href="#home">Ranking</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
              <Nav.Link href="#history">History</Nav.Link>
              <Nav.Link href="#report">Report</Nav.Link>
            </Nav>
            <RewardModal />
          </Navbar.Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default NavigationBar;
