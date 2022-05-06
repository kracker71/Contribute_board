import React, { Component } from "react";
import "./RewardModal.css";
import { Modal, Button } from "react-bootstrap";
import RewardList from "../RewardList/RewardList";
import rewardImg from "./reward.png";

const rewardList = [];

for (let i = 1; i <= 3; i++) {
  const rewardInfo = {
    img: rewardImg,
    desc: `ของรางวัล ${i}`,
  };
  rewardList.push(rewardInfo);
}

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
        <Button variant="custom" onClick={this.handleShow}>
          ของรางวัล
        </Button>

        <Modal
          className="reward-modal"
          dialogClassName="modal-90w"
          show={this.state.show}
          onHide={this.handleClose}
          centered
        >
          <Modal.Header>
            <Modal.Title>ของรางวัลประจำเดือน พฤษภาคม 2565</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <RewardList rewardList={rewardList} />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              ปิด
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

export default RewardModal;
