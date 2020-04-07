import React from 'react';
import { Component, Link } from 'react'
import { connect } from "react-redux"
import { Button, Card, Row, Col } from 'react-bootstrap'
import './userWords.css'
import Header from "./header.js"
import WordCards from "./wordCards.js"
import * as actions from "../actions/index.js"
import Modal from 'react-bootstrap/Modal'
import IntroUserWords from "./intros/userWords.js"


class UserWords extends Component {
    constructor() {
        super()

        this.state = {
            showIntroModal: false
        }
    }


    async componentDidMount() {
        this.props.getWords(this.props.viewNum, this.props.startPost)
        await this.props.getUser()
    }

    renderButtons() {
        if (this.props.startPost > 9 && this.props.startPost <= 90 ) {
            return (
                <Row>
                    <Col xs={1}></Col>
                        <Col xs={10}>
                            <Button className="words-less-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                            <Button className="words-more-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>
                        </Col>
                    <Col xs={1}></Col>
                </Row>  
            )
        } else if (this.props.startPost < 10) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="words-more-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost + 10)); this.props.incrementPostNumber(this.props.viewNum); window.scrollTo(0, 0)}}>Next</Button>                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        } else if (this.props.startPost > 90) {
            return (
                <Row>
                    <Col xs={2}></Col>
                        <Col xs={8}>
                            <Button className="words-less-words" onClick={event => { this.props.getWords(this.props.viewNum, (this.props.startPost - 10)); this.props.decrementPostNumber(this.prps.viewNum); window.scrollTo(0, 0)}}>Back</Button>
                        </Col>
                    <Col xs={2}></Col>
                </Row>  
            )
        }
    }

    async checkNewUser() {
        if (Object.keys(this.props.user).length > 0) {
            if ((!this.props.user.visited.includes("/user/words")) && (this.state.showIntroModal == false)) {
                this.setState({showIntroModal: true})
                await this.props.addRoomToUser("/user/words")
            }
        }
    }

    render() {
        this.checkNewUser()
        if (this.props.words.length == 0) {
            return (
                <div>
                    <Header />
                    <Modal
                            className="intro-modal"
                            size={"s"} 
                            show={this.state.showIntroModal} 
                            onHide={() => {this.setState({showIntroModal:false})}}>
                            <Modal.Body class="intro-body">
                                <IntroUserWords></IntroUserWords>
                            </Modal.Body>
                        </Modal>
                    <Row>
                        <Col xs={4}></Col>
                        <Col xs={4}>
                            <h2 className="loading">Loading Words!</h2>
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
                                <IntroUserWords></IntroUserWords>
                            </Modal.Body>
                        </Modal>
                        <Row>
                            <Col xs={2}></Col>
                                <Col xs={8}>
                                    <Button className="words-read-words" href="/user/words">Read</Button>
                                    <Button className="words-study-words" href="/user/words/study">Study</Button>
                                </Col>
                            <Col xs={2}></Col>
                        </Row>  
                        <WordCards />
                        { this.renderButtons() }
                    </div>
                )
            }
        }
}

function mapStateToProps(state) {
    return {
        words: state.words,
        viewNum: state.viewNum,
        startPost: state.startPost,
        user: state.user
    }
}

export default connect(mapStateToProps, actions)(UserWords)