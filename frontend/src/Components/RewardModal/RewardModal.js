import React, { Component } from "react";
import { Modal, Button } from "react-bootstrap";
import RewardTitle from "../RewardTitle/RewardTitle";
import RewardList from "../RewardList/RewardList";

class RewardModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false,
    };
  }

  handleClose = () => {
    this.setState({ show: false });
  };

  handleShow = () => {
    this.setState({ show: true });
  };

  render() {
    return (
      <div className="RewardModal">
        <Button variant="primary" onClick={this.handleShow}>
          ของรางวัล
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>
              <RewardTitle />
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <RewardList />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

export default RewardModal;
