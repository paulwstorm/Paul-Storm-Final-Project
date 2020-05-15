import React from 'react';
import { Component } from 'react'
import { Button, Row, Col } from 'react-bootstrap'
import './userPage.css'
import Header from "./header.js"
import Modal from 'react-bootstrap/Modal'
import IntroUser from "./intros/user.js"
import { connect } from "react-redux"
import * as actions from "../actions/index.js"

class UserPage extends Component{
    constructor() {
        super()

        this.state = {
            showIntroModal: false
        }
    }

    async componentDidMount() {
        await this.props.getUser()
    }

    async checkNewUser() {
        if (Object.keys(this.props.user).length > 0) {
            if ((!this.props.user.visited.includes("/user")) && (this.state.showIntroModal == false)) {
                this.setState({showIntroModal: true})
                await this.props.addRoomToUser("/user")
            }
        }
    }

    render() {
        this.checkNewUser()
        return (
            <div>
                <Header />
                <Modal
                    className="intro-modal"
                    size={"s"} 
                    show={this.state.showIntroModal} 
                    onHide={() => {this.setState({showIntroModal:false})}}>
                    <Modal.Body class="intro-body">
                        <IntroUser></IntroUser>
                    </Modal.Body>
                </Modal>
                <Row>
                    <Col xs={4}></Col>
                    <Col className={"user-page-buttons"} xs={4}>
                        <div><Button className={"my-clozes"} href="/user/clozes"> My Clozes</Button></div>
                        <div><Button className={"my-words"} href="/user/words">My Words</Button></div>
                    </Col>
                    <Col xs={4}></Col>
                </Row>
            </div>
        )
    }

}

function mapStateToProps(state) {
    return {
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(UserPage)