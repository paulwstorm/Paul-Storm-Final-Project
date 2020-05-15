import React from 'react';
import { Component } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './userClozes.css'
import Header from "./header.js"
import PostClozeCards from "./postClozeCards.js"
import * as actions from "../actions/index.js"
import IntroUserClozes from "./intros/userClozes.js"
import Modal from 'react-bootstrap/Modal'

class UserClozes extends Component{
    constructor () {
        super()

        this.state = {
            show: false,
            view: "incorrect",
            incorrectButton: "button-on",
            allButton: "button-off",
            showIntroModal: false
        }
    }

    async componentDidMount() {
        this.props.getUserClozes(this.props.viewNum, this.props.startPost, this.state.view)
        await this.props.getUser()

    }

    async handleToggleClick(view) {
        await this.setState({view: view})
        this.props.getUserClozes(this.props.viewNum, this.props.startPost, this.state.view)
    }

    renderButtons() {
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="posts-clozes-less-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="posts-clozes-more-posts" onClick={event => { this.props.getPostClozes(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="posts-clozes-more-posts" onClick={event => { this.props.getUserClozes(this.props.viewNum, (this.props.startPost + 10), this.state.view); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                <Col xs={2}></Col>
                    <Col xs={8}>
                        <Button className="lposts-clozes-less-posts" onClick={event => { this.props.getUserClozes(this.props.viewNum, (this.props.startPost - 10), this.state.view); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                    </Col>
                <Col xs={2}></Col>
            </Row>  
            )
        }
    }

    async checkNewUser() {
        if (Object.keys(this.props.user).length > 0) {
            if ((!this.props.user.visited.includes("/user/clozes")) && (this.state.showIntroModal == false)) {
                this.setState({showIntroModal: true})
                await this.props.addRoomToUser("/user/clozes")
            }
        }
    }

    render() {
        this.checkNewUser()
        if (Object.keys(this.props.user).length == 0) {
            return (
                <div>
                <Header />
                <Modal
                    className="intro-modal"
                    size={"s"} 
                    show={this.state.showIntroModal} 
                    onHide={() => {this.setState({showIntroModal:false})}}>
                    <Modal.Body class="intro-body">
                        <IntroUserClozes></IntroUserClozes>
                    </Modal.Body>
                </Modal>
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className={this.state.incorrectButton} onClick={() => {this.handleToggleClick("incorrect"); this.setState({allButton: "button-off"}); this.setState({incorrectButton: "button-on"})}}>Incorrect</Button>
                            <Button className={this.state.allButton} onClick={() => {this.handleToggleClick("all"); this.setState({incorrectButton: "button-off"}); this.setState({allButton: "button-on"})}}>All</Button>
                        </Col>
                    <Col xs={2}></Col>
                </Row>  
                <Row>
                    <Col xs={4}></Col>
                    <Col xs={4}>
                        <h2 className="loading">Loading your saved posts!</h2>
                    </Col>
                    <Col xs={4}></Col>
                </Row>
            </div>
            )
        } else if (this.props.clozes.length == 0) {
            return (
                <div>
                    <Header />
                    <Modal
                        className="intro-modal"
                        size={"s"} 
                        show={this.state.showIntroModal} 
                        onHide={() => {this.setState({showIntroModal:false})}}>
                        <Modal.Body class="intro-body">
                            <IntroUserClozes></IntroUserClozes>
                        </Modal.Body>
                    </Modal>
                    <Row>
                        <Col xs={2}></Col>
                            <Col xs={8}>
                                <Button className={this.state.incorrectButton} onClick={() => {this.handleToggleClick("incorrect"); this.setState({allButton: "button-off"}); this.setState({incorrectButton: "button-on"})}}>Incorrect</Button>
                                <Button className={this.state.allButton} onClick={() => {this.handleToggleClick("all"); this.setState({incorrectButton: "button-off"}); this.setState({allButton: "button-on"})}}>All</Button>
                            </Col>
                        <Col xs={2}></Col>
                    </Row>  
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">You don't have any saved posts!</h2>
                            <p>Click on the "+" button on any posts to save it</p>
                            <p>or play the fill-in-blank challenge and any posts you guess with be saved to your posts.</p>
                        </Col>
                        <Col xs={4}></Col>
                    </Row>
                </div>
            )} else {
                return (
                    <div>
                        <Header />
                        <Modal
                            className="intro-modal"
                            size={"s"} 
                            show={this.state.showIntroModal} 
                            onHide={() => {this.setState({showIntroModal:false})}}>
                            <Modal.Body class="intro-body">
                                <IntroUserClozes></IntroUserClozes>
                            </Modal.Body>
                        </Modal>
                        <Row>
                            <Col xs={2}></Col>
                                <Col xs={8}>
                                    <Button className={this.state.incorrectButton} onClick={() => {this.handleToggleClick("incorrect"); this.setState({allButton: "button-off"}); this.setState({incorrectButton: "button-on"})}}>Incorrect</Button>
                                    <Button className={this.state.allButton} onClick={() => {this.handleToggleClick("all"); this.setState({incorrectButton: "button-off"}); this.setState({allButton: "button-on"})}}>All</Button>
                                </Col>
                            <Col xs={2}></Col>
                        </Row>  
                        <PostClozeCards />
                        { this.renderButtons() }
                    </div>
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        clozes: state.clozes,
        viewNum: state.viewNum,
        startPost: state.startPost,
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(UserClozes)