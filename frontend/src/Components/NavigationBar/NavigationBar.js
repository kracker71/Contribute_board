import React, { Component } from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import "./NavigationBar.css";
import RewardModal from "../RewardModal/RewardModal";

class NavigationBar extends Component {
  render() {
    return (
      <div className="NavigationBar">
        <Navbar expand="md" variant="dark">
          <Container>
            <Navbar.Toggle />
            <Navbar.Collapse>
              <Nav className="me-auto">
                <Nav.Link href="#home">อันดับ</Nav.Link>
                <Nav.Link href="#about">ประวัติ</Nav.Link>
                <Nav.Link href="#history">เกี่ยวกับเรา</Nav.Link>
                <Nav.Link href="#report">รายงานปัญหา</Nav.Link>
              </Nav>
              <RewardModal />
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </div>
    );
  }
}

export default NavigationBar;
